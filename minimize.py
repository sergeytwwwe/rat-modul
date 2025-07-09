#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import platform
try:
    import win32gui
    import win32con
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
            import win32con
            # Находим окно рабочего стола и минимизируем его (это минимизирует все окна)
            desktop = win32gui.GetDesktopWindow()
            win32gui.ShowWindow(desktop, win32con.SW_MINIMIZE)
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка сворачивания всех окон: {e}")
        return False
