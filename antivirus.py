import platform
import subprocess
import logging
import psutil
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
    antivirus = []
    try:
        # Проверка Windows Defender
        try:
            result = subprocess.run(["sc", "query", "WinDefend"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if "RUNNING" in result.stdout:
                antivirus.append("Windows Defender (работает)")
        except:
            pass

        # Проверка через WMI
        try:
            cmd = 'wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /value'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.stdout.strip():
                for line in result.stdout.splitlines():
                    if line.startswith("displayName="):
                        av_name = line.split("=", 1)[1].strip()
                        if av_name:
                            antivirus.append(av_name)
        except:
            pass

        # Проверка через службы
        common_av_services = {
            "avast": "Avast Antivirus",
            "AVP": "Kaspersky",
            "bdss": "BitDefender",
            "ekrn": "ESET NOD32",
            "McAfee": "McAfee",
            "MsMpEng": "Microsoft Defender",
            "Sophos": "Sophos",
            "Symantec": "Norton",
            "Trend Micro": "Trend Micro"
        }

        try:
            result = subprocess.run(["sc", "query"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for service, name in common_av_services.items():
                if service in result.stdout:
                    antivirus.append(name)
        except:
            pass

        # Проверка через процессы
        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                if "avast" in proc_name:
                    antivirus.append("Avast Antivirus")
                elif "avg" in proc_name:
                    antivirus.append("AVG Antivirus")
                elif "kaspersky" in proc_name:
                    antivirus.append("Kaspersky")
                elif "bdagent" in proc_name:
                    antivirus.append("BitDefender")
                elif "egui" in proc_name or "ekrn" in proc_name:
                    antivirus.append("ESET NOD32")
                elif "mcshield" in proc_name:
                    antivirus.append("McAfee")
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
        try:
            result = subprocess.run(["clamscan", "--version"], capture_output=True, text=True)
            if "ClamAV" in result.stdout:
                av.append("ClamAV")
        except:
            pass
            
        # Проверка rkhunter
        try:
            result = subprocess.run(["rkhunter", "--version"], capture_output=True, text=True)
            if "Rootkit Hunter" in result.stdout:
                av.append("Rootkit Hunter")
        except:
            pass
            
        return av if av else ["Антивирусы не обнаружены"]
