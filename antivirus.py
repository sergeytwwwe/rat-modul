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
    antivirus = []
    try:
        # Проверка Windows Defender
        try:
            result = subprocess.run(["sc", "query", "WinDefend"], capture_output=True, text=True)
            if "RUNNING" in result.stdout:
                antivirus.append("Windows Defender")
        except:
            pass

        # Проверка через PowerShell
        try:
            ps_command = "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName"
            result = subprocess.run(["powershell", "-Command", ps_command], capture_output=True, text=True)
            if result.stdout.strip():
                for line in result.stdout.splitlines():
                    if line.strip() and "displayName" not in line:
                        antivirus.append(line.strip())
        except:
            pass

        # Проверка через реестр
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
                for i in range(0, winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "antivirus" in name.lower() or "security" in name.lower() or "avast" in name.lower() or "kaspersky" in name.lower():
                                    antivirus.append(name)
                            except WindowsError:
                                pass
                    except WindowsError:
                        pass
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
