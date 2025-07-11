import platform
import subprocess
import logging
import psutil
import os
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
        # 1. Проверка через WMI (основной метод)
        try:
            cmd = 'wmic /namespace:\\\\root\\SecurityCenter2 path AntiVirusProduct get displayName /value'
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if result.stdout.strip():
                for line in result.stdout.splitlines():
                    if line.startswith("displayName="):
                        av_name = line.split("=", 1)[1].strip()
                        if av_name:
                            antivirus.append(av_name)
        except Exception as e:
            logger.error(f"WMI detection error: {e}")

        # 2. Проверка через службы
        av_services = {
            "360sd": "360 Total Security",
            "360tray": "360 Total Security",
            "ZhuDongFangYu": "360 Safeguard",
            "avast": "Avast Antivirus",
            "AVP": "Kaspersky",
            "bdss": "BitDefender",
            "egui": "ESET NOD32",
            "ekrn": "ESET NOD32",
            "McAfee": "McAfee",
            "MsMpEng": "Microsoft Defender",
            "Sophos": "Sophos",
            "Symantec": "Norton",
            "Trend Micro": "Trend Micro",
            "QBVSS": "Quick Heal",
            "avguard": "Avira",
            "hipsdaemon": "Comodo"
        }

        try:
            result = subprocess.run(["sc", "query"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            for service, name in av_services.items():
                if service in result.stdout:
                    antivirus.append(name)
        except Exception as e:
            logger.error(f"Service detection error: {e}")

        # 3. Проверка через процессы
        av_processes = {
            "360sd.exe": "360 Total Security",
            "360tray.exe": "360 Total Security",
            "zhudongfangyu.exe": "360 Safeguard",
            "avastui.exe": "Avast",
            "avgui.exe": "AVG",
            "avp.exe": "Kaspersky",
            "bdagent.exe": "BitDefender",
            "egui.exe": "ESET NOD32",
            "mcshield.exe": "McAfee",
            "msseces.exe": "Microsoft Defender",
            "sophosui.exe": "Sophos",
            "ccsvchst.exe": "Norton",
            "tmproxy.exe": "Trend Micro",
            "avira.exe": "Avira",
            "cmdagent.exe": "Comodo"
        }

        try:
            for proc in psutil.process_iter(['name']):
                proc_name = proc.info['name'].lower()
                for exe, name in av_processes.items():
                    if exe.lower() == proc_name:
                        antivirus.append(name)
        except Exception as e:
            logger.error(f"Process detection error: {e}")

        # 4. Проверка через пути установки
        install_paths = {
            "360TotalSecurity": "360 Total Security",
            "Avast Software": "Avast",
            "AVG": "AVG",
            "Kaspersky Lab": "Kaspersky",
            "BitDefender": "BitDefender",
            "ESET": "ESET NOD32",
            "McAfee": "McAfee",
            "Sophos": "Sophos",
            "Norton": "Norton",
            "Trend Micro": "Trend Micro",
            "Avira": "Avira",
            "Comodo": "Comodo"
        }

        try:
            program_files = os.getenv("ProgramFiles")
            program_files_x86 = os.getenv("ProgramFiles(x86)") or program_files
            
            for path in [program_files, program_files_x86]:
                if path:
                    for folder, name in install_paths.items():
                        if os.path.exists(os.path.join(path, folder)):
                            antivirus.append(name)
        except Exception as e:
            logger.error(f"Install path detection error: {e}")

        # 5. Проверка Windows Defender отдельно
        try:
            result = subprocess.run(["sc", "query", "WinDefend"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            if "RUNNING" in result.stdout:
                antivirus.append("Windows Defender (работает)")
        except Exception as e:
            logger.error(f"Windows Defender detection error: {e}")

        # Удаляем дубликаты и проверяем результаты
        unique_av = list(set(antivirus))
        return unique_av if unique_av else ["Антивирусы не обнаружены"]
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

        # Проверка chkrootkit
        try:
            result = subprocess.run(["chkrootkit", "-V"], capture_output=True, text=True)
            if "chkrootkit" in result.stdout:
                av.append("chkrootkit")
        except:
            pass
            
        return av if av else ["Антивирусы не обнаружены"]
    except Exception as e:
        logger.error(f"Linux AV detection failed: {e}")
        return ["Ошибка проверки антивирусов"]
