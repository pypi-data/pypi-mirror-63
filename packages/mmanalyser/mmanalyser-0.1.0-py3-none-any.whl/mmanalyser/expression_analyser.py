from mmanalyser import config
import re
import numpy as np
from pydub import AudioSegment
from mmanalyser.utils.nlu_tools import NluTools
import logging


WORD_SEP = '#'
AUDIO_START_TIME = 500


class ExpressionAnalyser:
    '''
    表达能力分析器

    asr数据格式：{"pause_detection": [[3280, 3922], [7781, 8688]], "text_corrected":  [], "text":  [[[0, 1170], "领导你好，"],[[8940, 12250], "我在嘉兴，"], [[12250, 13490], "有两家造纸厂，"]]}
    '''
    def __init__(self, rationality_service_url=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rationality_service_url = rationality_service_url
        self.nlu = NluTools()

    def get_expression_score(self, asr, audio_path=None):
        """
        获取表达能力分数

        Args:
            asr: asr结果
            audio_path:  音频地址

        Returns:
             dict: {
            'talk_speed': float,        // 语速
            'audio_clear': bool,        //声音是否清晰
            'mandarin_score': float,    //普通话标准程度
            'expression_score': float,  //表达能力分数
            }
        """
        raw_text, recognition_duration, pause_moment =\
                self.__get_text_information_from_asr(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count =\
                self.__disfluency_detection(raw_text)
        mandarin_score = self.__parse_mandarin_score(text)
        talk_speed = self.__get_talk_speed(text_length, recognition_duration)
        audio_clear = self.__is_audio_clear(audio_path, text_length, recognition_duration, mandarin_score)
        express_score = self.__parse_expression_score(
            audio_clear, text_length, pause_moment, recognition_duration,
            particle_count, mandarin_score, repeat_one_count, ranhou_count) * 20
        return {
            'talk_speed': talk_speed,
            'audio_clear': audio_clear,
            'mandarin_score': mandarin_score*100,
            'expression_score': express_score,
        }

    def get_talk_speed(self, asr):
        '''
        获取语速指标

        Args:
            asr: asr 结果
        Returns:
           float: 语速
        '''
        raw_text, recognition_duration, pause_moment = \
            self.__get_text_information_from_asr(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count = \
            self.__disfluency_detection(raw_text)
        talk_speed = self.__get_talk_speed(text_length, recognition_duration)
        return talk_speed

    def get_mandarin_score(self, asr):
        '''
        获取普通话标准程度

        Args:
            asr: asr结果

        Returns:
            float: 普通话标准程度
        '''
        raw_text, recognition_duration, pause_moment = \
            self.__get_text_information_from_asr(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count = \
            self.__disfluency_detection(raw_text)
        mandarin_score = self.__parse_mandarin_score(text)
        return mandarin_score

    def get_audio_clear(self, asr, audio_path):
        '''
        获取声音是否清晰

        Args:
            asr: asr结果
            audio_path: 音频地址

        Returns:
            bool: 清晰返回true 不清晰返回false
        '''
        raw_text, recognition_duration, pause_moment = \
            self.__get_text_information_from_asr(asr)
        text, text_length, particle_count, repeat_one_count, ranhou_count = \
            self.__disfluency_detection(raw_text)
        mandarin_score = self.__parse_mandarin_score(text)
        audio_clear = self.__is_audio_clear(audio_path, text_length, recognition_duration, mandarin_score)
        return audio_clear

    def __get_talk_speed(self, text_length, recognition_duration):
        self.logger.debug("get talk speed")
        return text_length / recognition_duration

    def __is_audio_clear(self, audio_path, length, recognition_duration, mandarin_score):
        self.logger.debug("get audio clear")
        if self.rationality_service_url is None:
            mandarin_score = 0.5

        flag = (mandarin_score != 0 and recognition_duration > 0 and (length / recognition_duration > 0.75 or
                                                                      (length / recognition_duration < 0.75 and mandarin_score > 0.5)))
        if audio_path is not None:
            dBFS_var, dBFS_mean = self.__get_dBFS_information(audio_path)
            return bool(dBFS_mean < config.voice_dBFS_human_max and
                    dBFS_var > config.voice_dBFS_human_var_min and flag)
        else:
            return flag

    def __parse_mandarin_score(self, text):
        self.logger.debug("parse mandarin score")
        if self.rationality_service_url is None:
            return -1

        sentences = self.__preprocess_text_for_ppl(text)
        if not sentences:
            return 0
        ppls = self.nlu.get_rationality(sentences, self.rationality_service_url)
        # 句子合理性 0~1分
        ppl_mark = 0
        for ppl in ppls:
            if ppl < config.voice_ppl_min:
                ppl_mark += 1
            elif ppl < config.voice_ppl_max:
                voice_ppl_range = config.voice_ppl_max - config.voice_ppl_min
                voice_ppl_diff = ppl - config.voice_ppl_min
                ppl_mark += 1 - voice_ppl_diff / voice_ppl_range
        return ppl_mark / (len(ppls)+0.2) if ppls else 0

    def __parse_expression_score(
            self,
            audio_clear,
            text_length,
            pause_moment,
            recognition_duration,
            particle_count,
            mandarin_score,
            repeat_one_count,
            ranhou_count):
        self.logger.debug("get expression score")
        if not audio_clear:
            return 0

        if self.rationality_service_url is None:
            mandarin_score = 0.5

        if len(pause_moment) == 0:
            recognition_duration_per_pause_count = config.voice_recognition_duration_per_pause_count_max
        else:
            recognition_duration_per_pause_count = text_length / \
                len(pause_moment)

        recognition_duration_per_pause_count_score = self.__min_max_scaler(
            recognition_duration_per_pause_count,
            config.voice_recognition_duration_per_pause_count_min,
            config.voice_recognition_duration_per_pause_count_max)
        pause_duration_ratio = sum(pause_moment) / recognition_duration if recognition_duration > 0 else 1
        pause_duration_ratio_score = self.__min_max_scaler(
            pause_duration_ratio,
            config.voice_pause_duration_ratio_min,
            config.voice_pause_duration_ratio_max,
            negative=True)

        # 语气词 0~1分
        if particle_count == 0:
            length_per_count = config.voice_length_per_count_max
        else:
            length_per_count = text_length / particle_count
        length_per_count_score = self.__min_max_scaler(
            length_per_count, config.voice_length_per_count_min,
            config.voice_length_per_count_max)
        repeat_one_count_score = self.__min_max_scaler(
            repeat_one_count,
            config.voice_repeat_one_count_min,
            config.voice_repeat_one_count_max,
            negative=True)

        ranhou_count_per_length = ranhou_count / text_length
        ranhou_count_per_length_score = self.__min_max_scaler(
            ranhou_count_per_length, 0.02, 0.06, negative=True)

        decay_factor = 0.8 if pause_duration_ratio_score == 0 or \
            recognition_duration_per_pause_count_score == 0 or \
            length_per_count_score == 0 or \
            repeat_one_count_score == 0 else 1

        return (0.75 * pause_duration_ratio_score + 0.75 *
                recognition_duration_per_pause_count_score + 1.5 * length_per_count_score +
                1.5 * repeat_one_count_score + ranhou_count_per_length_score * 0.5) * decay_factor * (0.85 + 0.1 * mandarin_score/100)

    def __get_text_information_from_asr(self, asr):
        recognition_duration = sum(
            [int(x[0][1]) - int(x[0][0]) for x in asr['text']]) / 1000
        # 停顿
        pause_moment = [(x[0]-x[1])/1000 for x in asr["pause_detection"] if x[1] - x[0] > 500]
        text = ''.join([x[1] for x in asr['text']])
        return text, recognition_duration, pause_moment

    def __disfluency_detection(self, text):
        # 语气词
        particle_count = len(
            re.findall(config.voice_modal_particles_pattern,
                       re.sub(config.text_clean_for_modal_particles, '', text)))

        # 文本清理
        text = re.sub(config.text_clean_for_ppl, WORD_SEP, text)

        _text = text.replace(WORD_SEP, '')
        repeat_one_count = len(self.__get_repeat_record_by_offset(_text, 1))
        ranhou_count = len(re.findall('然后', _text))
        text_length = len(_text)
        return text, text_length, particle_count, repeat_one_count, ranhou_count

    def __get_dBFS_information(self, audio):
        sound = AudioSegment.from_file(audio, "mp3")
        dBFS = []
        for x in range(AUDIO_START_TIME, len(sound),
                       config.voice_dBFS_sample_interval):
            dbfs = sound[x:x + config.voice_dBFS_sample_interval].dBFS
            if dbfs != float("-inf"):
                dBFS.append(dbfs)
        return np.var(dBFS), np.mean(dBFS)

    def __preprocess_text_for_ppl(self, text):
        MAX_SENTENCE_LEN = 5
        MIN_SENTENCE_LEN = 2

        def need_concate_sentence(word, sentence):
            not_has_start_words = all(
                [prefix not in word for prefix in config.start_word4ppl])
            return not_has_start_words and len(sentence) <= MAX_SENTENCE_LEN

        def has_skip_word(sentence):
            return any(
                [skip_word in sentence for skip_word in config.skip_word4ppl])
        words = text.split(WORD_SEP)
        sentences = []
        sentence = ""
        for word in words:
            if need_concate_sentence(word, sentence):
                sentence += word
            else:
                if len(sentence) > MIN_SENTENCE_LEN:
                    sentences.append(sentence)
                sentence = word
        if len(sentence) > MIN_SENTENCE_LEN:
            sentences.append(sentence)
        _sentences = [sent for sent in sentences if not has_skip_word(sent)]
        if len(_sentences) == 0:
            _sentences = sentences
        return _sentences

    def __min_max_scaler(self, value, min_value, max_value, negative=False):
        score = 0
        if value > max_value:
            score = 1
        elif value > min_value:
            diff = value - min_value
            score += diff / (max_value - min_value)
        return score if not negative else 1 - score


    def __get_repeat_record_by_offset(self, text, offset=1):
        assert offset > 0
        length = len(text)
        repeat_record = []
        word = text[0:offset] if length > 0 else ''
        i = offset * 2
        count = 1
        while i < length + 1:
            if word == text[i - offset:i]:
                count += 1
            else:
                if count > 1:
                    repeat_record.append(count)
                i = i - offset + 1
                count = 1
                word = text[i - offset:i]
            i = i + offset
        if count > 1:
            repeat_record.append(count)
        return repeat_record


if __name__ == '__main__':
    ea = ExpressionAnalyser()
    fake_asr = {
        "pause_detection": [[3280, 3922], [7781, 8688]],  # 停顿检测结果
        "text_corrected":  [[[0, 1170], "领导你好，"], [[1170, 2370], "我叫秦嘉涵，"], [[2370, 5530], "今年26岁，"], [[5530, 8040], "是浙江龙游人，"], [[8040, 8940], "我，"], [[8940, 12250], "我在龙游，"], [[12250, 13490], "有两家造纸厂，"], [[13490, 19330], "有4年的维修工禁令。"]],
        "text":  [[[0, 1170], "领导你好，"], [[1170, 2370], "我叫秦嘉涵，"], [[2370, 5530], "今年26岁，"], [[5530, 8040], "是浙江龙游人，"], [[8040, 8940], "我，"], [[8940, 12250], "我在龙游，"], [[12250, 13490], "有两家造纸厂，"], [[13490, 19330], "有4年的维修工禁令。"]]
    }
    print(ea.get_expression_score(asr=fake_asr, verbose=True))






