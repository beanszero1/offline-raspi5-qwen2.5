# -*- coding: utf-8 -*-

import os
import time
import sys

import config
import keyboard_listener
import asr
import model_api
import tts
import check_utils
import logging_utils

# 设置日志记录
logger = logging_utils.setup_module_logging("main")

def check_services():
    """检查所需服务是否可用"""
    print("检查系统服务...")
    logger.info("检查系统服务...")
    
    # 使用check_utils检查所有服务
    if not check_utils.check_all_services():
        return False
    
    return True



def process_recorded_audio():
    """处理已录音的音频缓冲区"""
    if len(config.audio_buffer) == 0:
        sys.stdout.write("\r录音缓冲区为空，跳过处理\n")
        sys.stdout.flush()
        return
    
    sys.stdout.write(f"\r处理录音数据，长度: {len(config.audio_buffer)} 字节\n")
    sys.stdout.flush()
    
    # 调用ASR识别整个缓冲区
    text = asr.recognize_buffer(config.audio_buffer)
    
    if text and len(text) > config.MIN_TEXT_LENGTH - 1:
        sys.stdout.write(f"\r识别结果: {text}\n")
        sys.stdout.flush()
        
        # 简单唤醒词检测
        if any(keyword in text for keyword in config.WAKE_WORDS):
            sys.stdout.write("\r检测到对话意图，正在思考...\n")
            sys.stdout.flush()
            reply = model_api.ask_ai(text)
            tts.speak(reply)
        else:
            if len(text) > config.MIN_NON_WAKE_TEXT_LENGTH - 1:
                reply = model_api.ask_ai(text)
                tts.speak(reply)
    else:
        sys.stdout.write("\r未识别到有效语音\n")
        sys.stdout.flush()
    
    # 清空缓冲区以备下次录音
    config.audio_buffer.clear()

def main():
    """主循环"""
    print("\n语音助手就绪！")
    print("提示：按下 空格键 开始/停止录音，按下 Q 键可以退出程序")
    
    # 设置键盘监听
    old_settings = keyboard_listener.setup_keyboard_listener()
    
    try:
        while not config.exit_flag:
            # 检查键盘输入
            if keyboard_listener.check_key_press(old_settings):
                break
                
            # 检查是否有待处理的录音
            if config.processing_pending:
                process_recorded_audio()
                config.processing_pending = False
                
            # 检查音频输入
            data = asr.get_audio_data()
            if len(data) == 0: 
                continue

            # 如果在录音状态，将音频数据累积到缓冲区
            if config.recording_flag:
                config.audio_buffer.extend(data)
            # 不在录音状态时，不收集数据

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n用户中断，退出系统")
    except Exception as e:
        print(f"系统错误: {e}")
    finally:

        keyboard_listener.restore_keyboard_settings(old_settings)
        asr.cleanup_asr()
        print("资源清理完成")

if __name__ == "__main__":
    if check_services():
        main()
    else:
        print("服务检查失败，请解决上述问题后重试")
