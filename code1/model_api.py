# -*- coding: utf-8 -*-
"""
AI模型API模块
通过Ollama与模型进行交互
"""

import requests
import config

def ask_ai(text):

    try:
        # 尝试请求本地 LLM
        response = requests.post(config.OLLAMA_URL, json={
            "model": config.AI_MODEL,
            "messages": [
                {'role': 'system', 'content': config.SYSTEM_PROMPT},
                {'role': 'user', 'content': text}
            ],
            "stream": False
        }, timeout=config.AI_TIMEOUT)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['message']['content'].strip()
            return reply
        else:
            return "抱歉，AI服务暂时不可用"
            
    except requests.exceptions.ConnectionError:
        return "无法连接到AI服务，请检查Ollama是否启动"
    except requests.exceptions.Timeout:
        return "AI响应超时，请稍后再试"
    except Exception as e:
        return f"处理请求时出现错误: {str(e)}"
