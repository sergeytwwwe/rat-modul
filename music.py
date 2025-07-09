#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import requests
import threading
import time
from pydub import AudioSegment
from pydub.playback import play

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Глобальная переменная для управления воспроизведением
current_playback = None
stop_playback = False

def play_music(url):
    """Воспроизводит музыку из URL"""
    global current_playback, stop_playback
    
    try:
        logger.info(f"🎵 Получена команда: Воспроизвести музыку")
        
        # Скачиваем файл
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"❌ Ошибка скачивания файла: {response.status_code}")
            return False
        
        # Сохраняем временный файл
        filename = "temp_music.mp3"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Загружаем аудио
        audio = AudioSegment.from_file(filename, format="mp3")
        
        # Останавливаем предыдущее воспроизведение
        stop_playback = True
        if current_playback and current_playback.is_alive():
            current_playback.join(timeout=1)
        
        # Запускаем новое воспроизведение в отдельном потоке
        stop_playback = False
        current_playback = threading.Thread(target=play_audio, args=(audio,))
        current_playback.daemon = True
        current_playback.start()
        
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка воспроизведения музыки: {e}")
        return False

def play_audio(audio):
    """Воспроизводит аудио с возможностью остановки"""
    global stop_playback
    
    try:
        start_time = time.time()
        chunk_size = 100  # 100ms chunks
        
        # Воспроизводим по частям для возможности прерывания
        for i in range(0, len(audio), chunk_size):
            if stop_playback:
                break
                
            chunk = audio[i:i+chunk_size]
            play(chunk)
        
        duration = time.time() - start_time
        logger.info(f"✅ Музыка воспроизведена ({duration:.2f} сек)")
    except Exception as e:
        logger.error(f"❌ Ошибка в потоке воспроизведения: {e}")
