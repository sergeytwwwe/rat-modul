import logging
import time
from PIL import ImageGrab
import os

logger = logging.getLogger(__name__)

def take_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        ImageGrab.grab().save(filename)
        logger.info(f"📸 Скриншот сохранен: {filename}")
        return filename
    except Exception as e:
        logger.error(f"❌ Ошибка создания скриншота: {e}")
        return None
