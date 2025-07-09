#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def mute():
    """Выключает звук"""
    try:
        logger.info("🔇 Получена команда: Выключить звук")
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(1, None)
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка выключения звука: {e}")
        return False

def unmute():
    """Включает звук"""
    try:
        logger.info("🔊 Получена команда: Включить звук")
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(0, None)
        return True
    except Exception as e:
        logger.error(f"❌ Ошибка включения звука: {e}")
        return False
