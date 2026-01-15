# -*- coding: utf-8 -*-
"""
键盘监听模块
提供非阻塞键盘输入检测功能
"""

import sys
import select
import termios
import tty

import config

def setup_keyboard_listener():
    """设置非阻塞键盘输入"""
    # 保存当前终端设置
    old_settings = termios.tcgetattr(sys.stdin)
    # 设置非阻塞模式
    tty.setraw(sys.stdin.fileno())
    return old_settings

def check_key_press(old_settings):
    """检查是否有按键输入，只检测q键退出"""
    # 检查是否有键盘输入（非阻塞）
    if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
        key = sys.stdin.read(1)
        
        # 检测q键
        if key == 'q' or key == 'Q':
            print("\nQ键被按下，准备退出...")
            config.exit_flag = True
            return True
    
    return False

def restore_keyboard_settings(old_settings):
    """恢复终端设置"""
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
