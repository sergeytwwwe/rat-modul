#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import time
import logging
try:
    import win32gui
    import win32process
except ImportError:
    pass  # Для не-Windows систем

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def terminate_active_process():
    """Завершает активный процесс"""
    try:
        logger.info("💀 Получена команда: Завершить процесс")
        start_time = time.time()
        
        active_window = None
        if platform.system() == "Windows":
            window = win32gui.GetForegroundWindow()
            active_window = win32gui.GetWindowText(window)
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            process.terminate()
        
        execution_time = round(time.time() - start_time, 2)
        logger.info(f"✅ Процесс завершен за {execution_time} сек")
        return True, execution_time, active_window
    except Exception as e:
        logger.error(f"❌ Ошибка завершения процесса: {e}")
        return False, 0, None

def minimize_active_window():
    """Сворачивает активное окно"""
    try:
        if platform.system() == "Windows":
            window = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(window, 6)  # 6 = SW_MINIMIZE
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка сворачивания окна: {e}")
        return False

def minimize_all_windows():
    """Сворачивает все окна"""
    try:
        if platform.system() == "Windows":
            import win32con
            win32gui.ShowWindow(win32gui.GetDesktopWindow(), win32con.SW_MINIMIZE)
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка сворачивания всех окон: {e}")
        return False

def jiggle_mouse():
    """Двигает мышкой"""
    try:
        if platform.system() == "Windows":
            import win32api
            import random
            x, y = win32api.GetCursorPos()
            win32api.SetCursorPos((x + random.randint(-10, 10), y + random.randint(-10, 10))
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка движения мышки: {e}")
        return False
