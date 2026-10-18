import os
import time
import random
import pyttsx3
import PIL.Image
import pyautogui
import google.generativeai as genai

# Инициализация голосового движка
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print(f"\n[Голос]: {text}")
    engine.say(text)
    engine.runAndWait()

# Настройка API
genai.configure(api_key="YOUR_GEMINI_API_KEY")
# Используем 1.5-flash с высоким дневным лимитом
model = genai.GenerativeModel('gemini-1.5-flash')

desktop_path = os.path.expanduser("~/Desktop")

while True:
    try:
        print("\nГотовь экран! Пауза 3 секунды...")
        time.sleep(3)
        
        rand_id = random.randint(1000, 9999)
        screenshot_path = os.path.join(desktop_path, f"screen_{rand_id}.png")
        
        pyautogui.screenshot(screenshot_path)
        
        prompt = f"Кто или что изображено на этом скриншоте экрана? Опиши подробно. ReqID: {rand_id}"
        
        with PIL.Image.open(screenshot_path) as img:
            response = model.generate_content([prompt, img])
        
        result_text = response.text
        print("\n=== УСПЕХ! Ответ от сервера ===")
        print(result_text)
        
        speak("Скриншот успешно обработан!")
        speak(result_text[:700])
        
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
            
        print("\nСледующая проверка через 15 секунд...")
        time.sleep(15)  # Пауза между успешными запросами

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка/Перегрузка: {e}. Повтор через 20 сек...")
        time.sleep(20)  # Чтобы скрипт не атаковал сервер при ошибках
