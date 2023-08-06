# mmanalysis

`mmanalysis` 是多媒体特征分析工具的库

### 安装
```
$ pip install mmanalyser
```

#### ExpressionAnalyser

```python
class ExpressionAnalyser:
    '''
    表达能力分析器

    asr数据格式：{"pause_detection": [[3280, 3922], [7781, 8688]], "text_corrected":  [], "text":  [[[0, 1170], "领导你好，"],[[8940, 12250], "我在嘉兴，"], [[12250, 13490], "有两家造纸厂，"]]}
    '''
    
    def get_expression_score(self, asr, audio_path=None):
        '''
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
        '''


    def get_talk_speed(self, asr):
        '''
        获取语速指标
    
        Args:
            asr: asr 结果
        Returns:
           float: 语速
        '''


    def get_mandarin_score(self, asr):
        '''
        获取普通话标准程度
    
        Args:
            asr: asr结果
    
        Returns:
            float: 普通话标准程度
        '''
    
    def get_audio_clear(self, asr, audio_path):
        '''
        获取声音是否清晰
    
        Args:
            asr: asr结果
            audio_path: 音频地址
    
        Returns:
            bool: 清晰返回true 不清晰返回false
        '''
```

#### EmotionAnalyser

```python
class EmotionAnalyser:
    '''
    情绪分析器
    '''

    def get_emotion_global_distribution(self, emotion):
        """
    
        获取情绪的分布
    
        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]
    
        Returns:
            dict: distribution -> {'anger': 0.04678370220399322, 'neutral': 0.04147910314122111, 'disgust': 0.05076599764308418, 'fear': 0.012459961661656426, 'happiness': 0.3805726751609995, 'sadness': 0.001341534333740512, 'surprise': 0.46659702585530505}
        """


    def get_fluctuation_from_emotion(self, emotion):
        """
    
        获取情绪的波动
    
        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]
    
        Returns:
            list: fluction -> [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]
        """


    def parse(self, emotion):
        '''
        情绪整体分析，返回情绪数据，情绪总体分布，情绪波动
    
        Args:
            emotion: [{"anger": 0.1, "neutral": 0.1, "disgust": 0.1, "fear": 0.005670338961718315, "happiness": 0.2 "sadness": 0.1, "surprise": 0.2}, ...]
    
        Returns:
            list: data ->[[2.639, 1.415, 45.941, 3.918, 34.431, 0.159, 11.497], [0.685, 18.661, ... ] ... ]  顺序为['anger', 'neutral', 'disgust', 'fear', 'happiness', 'sadness', 'surprise']
            dict: distribution
            list: fluction
        '''
```

#### HeartRateAnalyser

```python
class HeartRateAnalyser:
    '''
    心率分析器
    '''
    def get_bpm_from_heart_rate(self, heart_rate):
        '''

        Args:
            heart_rate: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            list: [70, 71, ...] 平滑过的心率波动
        '''
```

#### FluctuationDetector

```python
class FluctuationDetector:
    '''
    波动检测器
    '''
    def get_abnormal_fluctuation_range_from_heart_rate(self, heart_rate_infos):
        '''
        从心率信息中抽取异常波动时间范围

        Args:
            heart_rate_infos: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            list: [start_time, end_time]
        '''

    def get_abnormal_fluctuation_range_from_emotion_fluction(self, emotion_fluctuation):
        '''
        从情绪波动信息中抽取异常波动时间范围

        Args:
            emotion_fluctuation: [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]

        Returns:
            list: [start_time, end_time]

        '''

    def get_text_from_emotion_abnormal_fluction(self, text_with_timestamp, emotion_fluctuation):
        '''
        结合带时间戳的文本抽取当情绪波动异常时的文本

        Args:
            text_with_timestamp: [[[[0, 1170], "领导你好，"], [[1170, 2370], "我叫，"]], ...]
            emotion_fluctuation: [0.2625822317841726, 0.286318327656083, 0.19226654361134174, 0.26339393328225225, 0.3021995866171042, 0.2843571171657221, ...]

        Returns
            str: "abnormal_text"
        '''
        
    def get_text_from_heart_rate_abnormal_fluction(self, text_with_timestamp, heart_rate):
        '''
        结合带时间戳的文本抽取心率波动异常时的文本

        Args:
            text_with_timestamp: [[[[0, 1170], "领导你好，"], [[1170, 2370], "我叫，"]], ...]
            heart_rate: [[70, 1000.0], [75, 2000.0], ...]

        Returns:
            str: "abnormal_text"
        '''
```
