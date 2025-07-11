#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import pyautogui

logger = logging.getLogger(__name__)

def press_key_combination(keys: str) -> str:
    """Нажимает комбинацию клавиш"""
    try:
        logger.info(f"⌨️ Получена команда: Нажать комбинацию клавиш {keys}")
        pyautogui.hotkey(*keys.split('+'))
        logger.info(f"✅ Комбинация клавиш {keys} нажата")
        return f"✅ Комбинация клавиш {keys} нажата"
    except Exception as e:
        logger.error(f"❌ Ошибка нажатия комбинации клавиш {keys}: {e}")
        return f"❌ Ошибка нажатия комбинации клавиш {keys}: {str(e)}"
