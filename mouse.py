#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
import platform
try:
    import win32api
    import win32con
except ImportError:
    pass  # Для не-Windows систем

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def jiggle_mouse():
    """Двигает мышкой"""
    try:
        logger.info("🖱 Получена команда: Дергать мышкой")
        if platform.system() == "Windows":
            x, y = win32api.GetCursorPos()
            # Делаем несколько случайных движений
            for _ in range(5):
                dx = random.randint(-20, 20)
                dy = random.randint(-20, 20)
                win32api.SetCursorPos((x + dx, y + dy))
                time.sleep(0.1)
            # Возвращаем курсор на место
            win32api.SetCursorPos((x, y))
            return True
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка движения мышки: {e}")
        return False
