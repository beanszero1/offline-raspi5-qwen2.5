# -*- coding: utf-8 -*-
"""
配置文件模块
包含常量配置和全局变量
"""

# --- 全局变量 ---
exit_flag = False
recording_flag = False  # 录音状态标志，空格键控制
audio_buffer = bytearray()  # 录音数据缓冲区
processing_pending = False  # 是否有待处理的录音缓冲区

# --- ASR配置 ---
# SenseVoice FastAPI 配置
SENSEVOICE_API_URL = "http://127.0.0.1:7860/api/v1/asr"  # FastAPI端点地址
SENSEVOICE_LANGUAGE = "auto"  
SENSEVOICE_TIMEOUT = 30  # API请求超时时间（秒）

# 音频参数（用于录音）
SAMPLE_RATE = 16000  # 音频采样率
FRAMES_PER_BUFFER = 4000  # 音频缓冲区大小
CHANNELS = 1  # 音频通道数
FORMAT = "pyaudio.paInt16"  # 音频格式

# --- TTS配置 ---
TTS_RATE = 200  # 语音合成语速
TTS_VOLUME = 0.8  # 语音合成音量

# --- AI模型配置 ---
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
OLLAMA_TAGS_URL = "http://127.0.0.1:11434/api/tags"
AI_MODEL = "qwen2.5:0.5b"     
AI_TIMEOUT = 15  # AI请求超时时间
SERVICE_CHECK_TIMEOUT = 5  # 服务检查超时时间

# --- 唤醒词配置 ---
WAKE_WORDS = ["助手", "你好", "请问", "帮助"]

# --- 百炼SDK配置 ---
BAILIAN_APP_ID = "a8877ad86xxxxxxf3486907efae88"
# nano ~/.bashrc
# API_KEY从环境变量DASHSCOPE_API_KEY读取


# --- 任务分类配置 ---
CLASSIFICATION_PROMPT = """
请判断以下问题类型：
1. 法律案例：涉及具体案件、违法行为、判罚、纠纷等（如：过马路撞到人、邻居噪音投诉、盗窃、金融犯罪）
2. 通用问题：日常对话、知识问答、闲聊等
3. 其他专业知识：特定领域专业知识（医学、工程、编程等）
只需回答"法律案例"、"通用问题"或"其他专业知识"。
"""

UNKNOWN_REPLY = "对不起，这个问题我不了解"  # 其他专业知识的回复

# --- TTS队列配置 ---
TTS_QUEUE_SIZE = 10  # TTS队列大小
TTS_STREAM_DELIMITERS = ["。", "，", "！", "？", "；", ".", ",", "!", "?", ";"]  # 句子分割符号

# --- 系统提示词 ---
SYSTEM_PROMPT = """
你是一个基础法律问答助手,作用是回答用户有关法律相关的问题。
请仔细理解用户的问题，然后给出有帮助的回答。
回答不要分点作答，用一句话概括。
回答要简洁，控制在30~50字之内。
重要：输出必须为纯文本，禁止使用任何特殊格式，包括但不限于：
- 星号(*)、下划线(_)、反斜杠等Markdown符号。
- LaTeX数学表达式。
- 加粗、斜体、代码块等任何格式化标记。
请直接以普通文本形式提供回答，避免任何符号或格式干扰。
不要简单地重复用户的问题，要进行思考并提供有用的信息。
如果用户的问题不清楚，可以请求澄清。
"""

# --- 音频处理配置 ---
MIN_TEXT_LENGTH = 2  # 最小文本长度
MIN_NON_WAKE_TEXT_LENGTH = 3 # 非唤醒词的最小文本长度
