# -*- coding: utf-8 -*-
"""
语音合成模块 (TTS)
使用 pyttsx3 进行离线语音合成
"""

import pyttsx3

# 全局变量
engine = None

def _init_engine():
    """初始化TTS引擎（内部函数）"""
    global engine
    if engine is not None:
        return
    
    engine = pyttsx3.init()

    # 自动寻找中文语音包
    voices = engine.getProperty('voices')
    found_zh = False
    for v in voices:
        if 'zh' in v.id or 'chinese' in v.name.lower():
            engine.setProperty('voice', v.id)
            found_zh = True
            print(f"TTS 已切换中文: {v.id}")
            break

    if not found_zh:
        try:
            engine.setProperty('voice', 'zh')
        except:
            pass

    engine.setProperty('rate', 165)  # 语速
    engine.setProperty('volume', 1.0) # 音量

def speak(text):
    """ 文字转语音输出 """
    global engine
    if engine is None:
        _init_engine()
    
    print(f"\n助手: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS 错误: {e}")
