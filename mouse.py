#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
import time
import platform

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def jiggle():
    """Двигает мышкой"""
    try:
        logger.info("🖱 Получена команда: Дергать мышкой")
        if platform.system() != "Windows":
            logger.warning("🖱 Функция доступна только на Windows")
            return False
        
        try:
            import win32api
        except ImportError as e:
            logger.error(f"❌ Не удалось импортировать win32api: {e}")
            return False

        x, y = win32api.GetCursorPos()
        for _ in range(10):
            dx = random.randint(-50, 50)
            dy = random.randint(-50, 50)
            win32api.SetCursorPos((x + dx, y + dy))
            time.sleep(0.05)
        win32api.SetCursorPos((x, y))
        logger.info("🖱 usurper: 🖱 Мышь успешно дернута")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка движения мышки: {e}")
        return False
