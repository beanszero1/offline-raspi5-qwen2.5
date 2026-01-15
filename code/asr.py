# -*- coding: utf-8 -*-
"""
语音识别模块 (ASR)
使用 Vosk 进行离线语音识别
"""

import os
import json
import pyaudio
import sys
from vosk import Model, KaldiRecognizer

import config

# 全局变量 - 延迟初始化
model = None
rec = None
p = None
stream = None

def _init_asr():
    """初始化语音识别"""
    global model, rec, p, stream
    
    if model is not None:
        return
    
    # 检查模型是否存在
    if not os.path.exists(config.MODEL_PATH):
        print(f"错误：找不到 '{config.MODEL_PATH}' 文件夹，请下载 Vosk 中文模型")
        exit(1)

    # 屏蔽冗余报错
    try:
        from ctypes import *
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        def py_error_handler(filename, line, function, err, fmt): pass
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
    except:
        pass


    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    
    try:
        print("正在加载 Vosk 离线模型...")
        model = Model(config.MODEL_PATH)
        rec = KaldiRecognizer(model, config.SAMPLE_RATE)
        p = pyaudio.PyAudio()

        # 打开麦克风流
        stream = p.open(
            format=pyaudio.paInt16,
            channels=config.CHANNELS,
            rate=config.SAMPLE_RATE,
            input=True,
            frames_per_buffer=config.FRAMES_PER_BUFFER,
            input_device_index=None,  # 让PyAudio自动选择
            input_host_api_specific_stream_info=None
        )
        stream.start_stream()
        
        # 恢复 stderr
        sys.stderr = old_stderr
        print("Vosk 模型加载完成")
    except Exception as e:
        # 恢复 stderr 并重新抛出异常
        sys.stderr = old_stderr
        raise e

def cleanup_asr():
    """清理语音识别资源"""
    global stream, p
    if stream:
        stream.stop_stream()
        stream.close()
    if p:
        p.terminate()

def get_audio_data():
    """获取音频数据（供主循环调用）"""
    global stream
    if stream is None:
        _init_asr()
    
    data = stream.read(config.FRAMES_PER_BUFFER, exception_on_overflow=False)
    return data

def recognize_audio(data):
    """识别音频数据"""
    global rec
    if rec is None:
        _init_asr()
    
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result['text'].replace(" ", "")
        return text
    
    return ""

