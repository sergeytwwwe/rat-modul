import ctypes
import platform
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def show_messagebox(title: str, text: str, style: str = "info") -> bool:
    """Показывает MessageBox на Windows"""
    try:
        if platform.system() != "Windows":
            return False
            
        styles = {
            "info": 0x40,       # MB_ICONINFORMATION
            "warning": 0x30,    # MB_ICONWARNING
            "error": 0x10,      # MB_ICONERROR
        }
        
        style_code = styles.get(style.lower(), 0x40)
        # Добавляем флаг MB_TASKMODAL (0x2000) чтобы убрать значок Python
        result = ctypes.windll.user32.MessageBoxW(0, text, title, style_code | 0x2000)
        return True
    except Exception as e:
        logger.error(f"MessageBox error: {e}")
        return False
