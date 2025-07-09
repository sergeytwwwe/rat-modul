import logging
import time
import cv2
import numpy as np
from mss import mss

logger = logging.getLogger(__name__)

def record_video(seconds):
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"video_{timestamp}.mp4"
        with mss() as sct:
            monitor = sct.monitors[1]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(filename, fourcc, 20.0, (monitor["width"], monitor["height"]))
            start_time = time.time()
            while (time.time() - start_time) < seconds:
                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                out.write(frame)
                time.sleep(0.05)
            out.release()
        logger.info(f"🎥 Видео сохранено: {filename}")
        return filename
    except Exception as e:
        logger.error(f"❌ Ошибка записи видео: {e}")
        return None
