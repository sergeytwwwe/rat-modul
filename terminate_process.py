#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psutil
import logging

logger = logging.getLogger(__name__)

def terminate_process_by_name(process_name: str) -> str:
    """Завершает процесс по имени, добавляя .exe, если указано без расширения"""
    try:
        logger.info(f"💀 Получена команда: Завершить процесс {process_name}")
        # Если имя без расширения, добавляем .exe
        if not process_name.lower().endswith('.exe'):
            process_name = f"{process_name}.exe"
        
        for proc in psutil.process_iter(['name']):
            if proc.info['name'].lower() == process_name.lower():
                proc.terminate()
                logger.info(f"✅ Процесс {process_name} завершен")
                return f"✅ Процесс {process_name} завершен"
        logger.warning(f"❌ Процесс {process_name} не найден")
        return f"❌ Процесс {process_name} не найден"
    except Exception as e:
        logger.error(f"❌ Ошибка завершения процесса {process_name}: {e}")
        return f"❌ Ошибка завершения процесса {process_name}: {str(e)}"
