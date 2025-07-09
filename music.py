#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import subprocess
import threading

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Глобальная переменная для управления воспроизведением
current_player = None

def play_music(url):
    """Воспроизводит музыку по URL"""
    global current_player
    
    try:
        logger.info(f"🎵 Воспроизведение музыки по URL: {url}")
        
        # Останавливаем предыдущее воспроизведение
        stop_music()
        
        # Определяем команду для воспроизведения в зависимости от ОС
        if os.name == 'nt':  # Windows
            command = f'start /MIN wmplayer "{url}"'
        else:  # Linux/Mac
            command = f'vlc --intf dummy "{url}"'
        
        # Запускаем воспроизведение в отдельном потоке
        def run_player():
            try:
                subprocess.run(command, shell=True, check=True)
            except Exception as e:
                logger.error(f"❌ Ошибка воспроизведения: {e}")
        
        player_thread = threading.Thread(target=run_player)
        player_thread.daemon = True
        player_thread.start()
        current_player = player_thread
        
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка воспроизведения музыки: {e}")
        return False

def stop_music():
    """Останавливает воспроизведение музыки"""
    global current_player
    
    try:
        # Останавливаем процессы плееров
        if os.name == 'nt':  # Windows
            os.system('taskkill /f /im wmplayer.exe >nul 2>&1')
        else:  # Linux/Mac
            os.system('pkill vlc >/dev/null 2>&1')
        
        # Останавливаем поток воспроизведения
        if current_player and current_player.is_alive():
            current_player.join(timeout=1)
            current_player = None
        
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка остановки музыки: {e}")
        return False
