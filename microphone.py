import sounddevice as sd
import numpy as np
import logging
import time
from scipy.io.wavfile import write

logger = logging.getLogger(__name__)

def record_audio(seconds: int) -> Optional[str]:
    """Записывает звук с микрофона"""
    try:
        fs = 44100  # Частота дискретизации
        timestamp = int(time.time())
        filename = f"audio_{timestamp}.wav"
        
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()  # Ждём окончания записи
        
        write(filename, fs, recording)
        return filename
    except Exception as e:
        logger.error(f"Audio recording error: {e}")
        return None
