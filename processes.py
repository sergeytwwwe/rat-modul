import psutil
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_process_list(limit: int = 50) -> List[Dict]:
    """Получает список процессов"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username', 'status', 'cpu_percent', 'memory_percent']):
            try:
                cpu = round(proc.info['cpu_percent'], 1)
                memory = round(proc.info['memory_percent'], 1)
                
                process_info = {
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'user': proc.info['username'],
                    'status': proc.info['status'],
                    'cpu': cpu,
                    'memory': memory,
                    'display': f"{proc.info['name']} (PID: {proc.info['pid']}, CPU: {cpu}%, Memory: {memory}%)"
                }
                processes.append(process_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        processes.sort(key=lambda x: x['cpu'], reverse=True)
        return processes[:limit]
    except Exception as e:
        logger.error(f"Process list error: {e}")
        return []

def kill_process(pid: int) -> bool:
    """Завершает процесс по PID"""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return True
    except Exception as e:
        logger.error(f"Kill process error: {e}")
        return False

def kill_process_by_name(process_name: str) -> bool:
    """Завершает процесс по имени"""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                return True
        return False
    except Exception as e:
        logger.error(f"Kill process by name error: {e}")
        return False
