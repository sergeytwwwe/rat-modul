#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import platform
import time
try:
    import win32gui
    import win32con
    import ctypes
except ImportError:
    pass  # Для не-Windows систем

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def minimize_active_window():
    """Сворачивает активное окно"""
    try:
        logger.info("⬇️ Получена команда: Свернуть активное окно")
        if platform.system() == "Windows":
            window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка сворачивания окна: {e}")
        return False

def minimize_all_windows():
    """Сворачивает все окна"""
    try:
        logger.info("📥 Получена команда: Свернуть все окна")
        if platform.system() == "Windows":
            # Используем комбинацию клавиш Win+D для сворачивания всех окон
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)  # Win
            ctypes.windll.user32.keybd_event(0x44, 0, 0, 0)  # D
            time.sleep(0.1)
            ctypes.windll.user32.keybd_event(0x44, 0, 2, 0)  # Release D
            ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)  # Release Win
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка сворачивания всех окон: {e}")
        return False
