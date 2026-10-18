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

# Настройка API (вставь свой ключ вместо заглушки)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-3.8-flash')

print("Запуск: скрипт сделает скриншот через 3 секунды...")

while True:
    try:
        print("\nГотовь экран! Пауза 3 секунды...")
        time.sleep(3)  # Задержка, чтобы успеть развернуть
        
        # 1. Делаем скриншот
        screenshot_path = "screen.png"
        pyautogui.screenshot(screenshot_path)
        
        # 2. Формируем запрос
        rand_id = random.randint(1000, 9999)
        prompt = f"Кто или что изображено на этом скриншоте экрана? Опиши подробно. ReqID: {rand_id}"
        
        # 3. Открываем картинку и отправляем в Gemini
        img = PIL.Image.open(screenshot_path)
        response = model.generate_content([prompt, img])
        
        result_text = response.text
        print("\n=== УСПЕХ! Ответ от сервера ===")
        print(result_text)
        
        speak("Скриншот успешно обработан!")
        speak(result_text[:700])  # Озвучить первые 700 символов
        
        break

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка/Перегрузка: {e}. Повтор через 2 сек...")
        time.sleep(2)
