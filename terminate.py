#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import time
import platform
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
