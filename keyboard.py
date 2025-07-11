#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import platform
import time
import pyautogui

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def press_combination(combination):
    """Нажимает комбинацию клавиш"""
    try:
        logger.info(f"⌨️ Получена команда: нажать комбинацию {combination}")
        
        # Обработка специальных клавиш
        special_keys = {
            'win': 'winleft',
            'ctrl': 'ctrl',
            'alt': 'alt',
            'shift': 'shift',
            'tab': 'tab',
            'esc': 'esc',
            'enter': 'enter',
            'space': 'space',
            'up': 'up',
            'down': 'down',
            'left': 'left',
            'right': 'right',
            'f1': 'f1',
            'f2': 'f2',
            'f3': 'f3',
            'f4': 'f4',
            'f5': 'f5',
            'f6': 'f6',
            'f7': 'f7',
            'f8': 'f8',
            'f9': 'f9',
            'f10': 'f10',
            'f11': 'f11',
            'f12': 'f12'
        }
        
        # Разбиваем комбинацию на отдельные клавиши
        keys = combination.lower().split('+')
        keys_to_press = []
        
        for key in keys:
            if key in special_keys:
                keys_to_press.append(special_keys[key])
            else:
                keys_to_press.append(key)
        
        # Нажимаем комбинацию
        pyautogui.hotkey(*keys_to_press)
        time.sleep(0.5)
        
        return f"✅ Комбинация {combination} успешно нажата"
    except Exception as e:
        logger.error(f"❌ Ошибка нажатия комбинации: {e}")
        return f"❌ Не удалось нажать комбинацию {combination}: {str(e)}"
