#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
import time
import platform
try:
    import win32api
except ImportError:
    pass

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
            for _ in range(10):
                dx = random.randint(-50, 50)
                dy = random.randint(-50, 50)
                win32api.SetCursorPos((x + dx, y + dy))
                time.sleep(0.05)
            win32api.SetCursorPos((x, y))
            logger.info("🖱 Мышь успешно дернута")
            return True
        logger.warning("🖱 Функция доступна только на Windows")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка движения мышки: {e}")
        return False
