# -*- coding: utf-8 -*-
"""
语音合成模块 (TTS)
使用 pyttsx3 进行离线语音合成
"""

import pyttsx3
import sys
import io
import logging_utils

from config import TTS_RATE,TTS_VOLUME

# 设置日志
logger = logging_utils.setup_module_logging("tts")

# 全局变量
engine = None


def speak(text):
    """ 文字转语音输出 """
    global engine
    if engine is None:
        _init_engine()

    sys.stdout.write('\r\n')
    sys.stdout.flush()
    sys.stdout.write(f'助手: {text}\n')
    sys.stdout.flush()
    
    # 临时重定向stdout和stderr以抑制pyttsx3运行时的输出
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    # 创建一个完全静默的StringIO对象
    silent_output = io.StringIO()
    sys.stdout = silent_output
    sys.stderr = silent_output
    
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        # 即使在静默模式下，也记录错误到日志
        logger.error(f"TTS 错误: {e}")
    finally:
        # 恢复stdout/stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        
        # 确保光标在新行开始
        sys.stdout.write('\n')
        sys.stdout.flush()



def _init_engine():
    global engine
    if engine is not None:
        return
    
    # 临时重定向stdout和stderr以抑制pyttsx3的所有输出
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    # 使用一个完全静默的StringIO对象
    silent_output = io.StringIO()
    sys.stdout = silent_output
    sys.stderr = silent_output
    
    try:
        # 在完全静默的环境中初始化TTS引擎
        engine = pyttsx3.init()
        
        # 继续在静默环境中设置语音属性
        voices = engine.getProperty('voices')
        found_zh = False
        for v in voices:
            if 'zh' in v.id or 'chinese' in v.name.lower():
                engine.setProperty('voice', v.id)
                found_zh = True
                # 只记录到日志，不输出到控制台
                logger.debug(f"TTS 已切换中文: {v.id}")
                break

        if not found_zh:
            try:
                engine.setProperty('voice', 'zh')
            except:
                pass

        engine.setProperty('rate', TTS_RATE)  
        engine.setProperty('volume', TTS_VOLUME)
        
    except Exception as e:
        # 恢复stdout/stderr后记录错误
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        logger.error(f"TTS引擎初始化失败: {e}")
        raise
    finally:
        # 确保恢复stdout/stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr
