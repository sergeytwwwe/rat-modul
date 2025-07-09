import os
import platform
import subprocess
import logging

logger = logging.getLogger(__name__)

def shutdown():
    """Выключение компьютера"""
    try:
        if platform.system() == "Windows":
            os.system("shutdown /s /t 1")
        else:
            os.system("shutdown -h now")
        return True
    except Exception as e:
        logger.error(f"Shutdown failed: {e}")
        return False

def reboot():
    """Перезагрузка компьютера"""
    try:
        if platform.system() == "Windows":
            os.system("shutdown /r /t 1")
        else:
            os.system("reboot")
        return True
    except Exception as e:
        logger.error(f"Reboot failed: {e}")
        return False
