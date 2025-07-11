import cv2
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

def capture_webcam_photo() -> Optional[str]:
    """Делает фото с веб-камеры"""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
            
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return None
            
        timestamp = int(time.time())
        filename = f"webcam_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        return filename
    except Exception as e:
        logger.error(f"Webcam photo error: {e}")
        return None

def record_webcam_video(seconds: int) -> Optional[str]:
    """Записывает видео с веб-камеры"""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = 20.0
        
        timestamp = int(time.time())
        filename = f"webcam_video_{timestamp}.avi"
        
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
        
        start_time = time.time()
        while (time.time() - start_time) < seconds:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
            else:
                break
                
        cap.release()
        out.release()
        return filename
    except Exception as e:
        logger.error(f"Webcam video error: {e}")
        return None
