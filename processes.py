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
                processes.append({
                    'name': proc.info['name'],
                    'pid': proc.info['pid'],
                    'user': proc.info['username'],
                    'status': proc.info['status'],
                    'cpu': proc.info['cpu_percent'],
                    'memory': proc.info['memory_percent']
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
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
