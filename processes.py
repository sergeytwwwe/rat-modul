import psutil
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

def get_process_list(page: int = 1, per_page: int = 5) -> Tuple[List[Dict], int, int]:
    """Получает список процессов с пагинацией"""
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
        
        total_processes = len(processes)
        total_pages = (total_processes + per_page - 1) // per_page
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        
        return processes[start_idx:end_idx], total_processes, total_pages
    except Exception as e:
        logger.error(f"Process list error: {e}")
        return [], 0, 0

def find_process_by_name(name: str) -> List[Dict]:
    """Ищет процессы по имени"""
    try:
        found = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    found.append({
                        'name': proc.info['name'],
                        'pid': proc.info['pid'],
                        'display': f"{proc.info['name']} (PID: {proc.info['pid']})"
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return found
    except Exception as e:
        logger.error(f"Find process error: {e}")
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
