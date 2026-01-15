# -*- coding: utf-8 -*-
"""
主程序模块
语音助手的主循环和服务检查
"""

import os
import time
import requests

import config
import keyboard_listener
import asr
import model_api
import tts

def check_services():
    """检查必要服务是否可用"""
    print("检查系统服务...")
    
    # 检查Vosk模型
    if not os.path.exists(config.MODEL_PATH):
        print(f"Vosk模型不存在，请下载中文模型到 '{config.MODEL_PATH}' 文件夹")
        return False
    
    # 检查Ollama服务
    try:
        response = requests.get(config.OLLAMA_TAGS_URL, timeout=config.SERVICE_CHECK_TIMEOUT)
        if response.status_code == 200:
            print("Ollama服务正常")
            models = response.json().get('models', [])
            if models:
                print(f"可用模型: {[m['name'] for m in models]}")
            else:
                print(f"没有找到模型，请先拉取模型: ollama pull {config.AI_MODEL}")
        else:
            print("Ollama服务异常")
            return False
    except:
        print("无法连接Ollama服务，请启动: ollama serve")
        return False
    
    return True

def main():
    """主循环"""
    print("\n语音助手就绪！请说话...")
    print("提示：按下 Q 键可以退出程序")
    tts.speak("语音助手启动完成，随时为您服务")
    
    # 设置键盘监听
    old_settings = keyboard_listener.setup_keyboard_listener()
    
    try:
        while not config.exit_flag:
            # 检查键盘输入
            if keyboard_listener.check_key_press(old_settings):
                break
                
            # 检查音频输入
            data = asr.get_audio_data()
            if len(data) == 0: 
                continue

            # Vosk 实时监听
            text = asr.recognize_audio(data)
            
            if text and len(text) > config.MIN_TEXT_LENGTH - 1:  # 过滤短噪音
                print(f"\n听到: {text}")
                
                # 简单唤醒词检测（可选）
                if any(keyword in text for keyword in config.WAKE_WORDS):
                    print("\n检测到对话意图，正在思考...")
                    reply = model_api.ask_ai(text)
                    print("\n")  # 空行分隔
                    tts.speak(reply)
                    print("\n")  # 空行分隔
                else:
                    # 非唤醒词也回复，但可以设置更宽松的条件
                    if len(text) > config.MIN_NON_WAKE_TEXT_LENGTH - 1:  # 只处理较长的语音
                        reply = model_api.ask_ai(text)
                        print("\n")  # 空行分隔
                        tts.speak(reply)
                        print("\n")  # 空行分隔

            # 短暂休眠以减少CPU占用
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n用户中断，退出系统")
    except Exception as e:
        print(f"系统错误: {e}")
    finally:
        # 清理资源
        keyboard_listener.restore_keyboard_settings(old_settings)
        asr.cleanup_asr()
        print("资源清理完成")

if __name__ == "__main__":
    if check_services():
        main()
    else:
        print("服务检查失败，请解决上述问题后重试")
