import platform
import subprocess
import logging
from typing import List

logger = logging.getLogger(__name__)

def detect_antivirus() -> List[str]:
    """Обнаруживает установленные антивирусы"""
    try:
        if platform.system() == "Windows":
            return _detect_windows_antivirus()
        elif platform.system() == "Linux":
            return _detect_linux_antivirus()
        else:
            return ["Проверка антивирусов для данной ОС не реализована"]
    except Exception as e:
        logger.error(f"Antivirus detection error: {e}")
        return ["Ошибка при проверке антивирусов"]

def _detect_windows_antivirus() -> List[str]:
    """Обнаружение антивирусов на Windows"""
    try:
        import wmi
        c = wmi.WMI()
        antivirus = []
        
        # Проверка через SecurityCenter2
        try:
            for item in c.Win32_Product():
                name = item.Name.lower()
                if "antivirus" in name or "security" in name or "avast" in name or "kaspersky" in name:
                    antivirus.append(item.Name)
        except:
            pass
            
        # Проверка через службы
        try:
            for service in c.Win32_Service():
                name = service.Name.lower()
                if "antivirus" in name or "avp" in name or "defender" in name:
                    antivirus.append(service.DisplayName)
        except:
            pass
            
        return list(set(antivirus)) if antivirus else ["Антивирусы не обнаружены"]
    except Exception as e:
        logger.error(f"Windows AV detection failed: {e}")
        return ["Ошибка проверки антивирусов"]

def _detect_linux_antivirus() -> List[str]:
    """Обнаружение антивирусов на Linux"""
    av = []
    try:
        # Проверка ClamAV
        result = subprocess.run(["clamscan", "--version"], capture_output=True, text=True)
        if "ClamAV" in result.stdout:
            av.append("ClamAV")
    except:
        pass
        
    try:
        # Проверка rkhunter
        result = subprocess.run(["rkhunter", "--version"], capture_output=True, text=True)
        if "Rootkit Hunter" in result.stdout:
            av.append("Rootkit Hunter")
    except:
        pass
        
    return av if av else ["Антивирусы не обнаружены"]
