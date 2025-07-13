#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import random
import time
import platform

logger = logging.getLogger(__name__)

# Проверка наличия pywin32
try:
    import win32api
    PYWIN32_AVAILABLE = True
except ImportError:
    PYWIN32_AVAILABLE = False
    logger.error("❌ Не установлен модуль pywin32. Установите его с помощью 'pip install pywin32'")

def jiggle():
    """Двигает мышкой"""
    try:
        logger.info("🖱 Получена команда: Дергать мышкой")
        if platform.system() != "Windows":
            logger.warning("🖱 Функция доступна только на Windows")
            return False
        if not PYWIN32_AVAILABLE:
            logger.error("❌ Модуль pywin32 не установлен, функция недоступна")
            return False
        
        x, y = win32api.GetCursorPos()
        for _ in range(10):
            dx = random.randint(-50, 50)
            dy = random.randint(-50, 50)
            win32api.SetCursorPos((x + dx, y + dy))
            time.sleep(0.05)
        win32api.SetCursorPos((x, y))
        logger.info("🖱 Мышь успешно дернута")
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка движения мышки: {e}")
        return False
