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
model = genai.GenerativeModel('gemini-3.8-flash')

print("Запуск: скрипт сам делает скриншот и отправляет в Gemini (интервал 2 сек)...")

while True:
    try:
        # 1. Делаем автоматический скриншот рабочего стола
        screenshot_path = "screen.png"
        pyautogui.screenshot(screenshot_path)
        
        # 2. Формируем запрос с уникальным ID
        rand_id = random.randint(1000, 9999)
        prompt = f"Кто или что изображено на этом скриншоте экрана? Опиши кратко и точно. ReqID: {rand_id}"
        
        # 3. Открываем сохранённый скриншот
        img = PIL.Image.open(screenshot_path)
        
        # 4. Отправляем запрос вместе с картинкой
        response = model.generate_content([prompt, img])
        
        result_text = response.text
        print("\n=== УСПЕХ! Ответ от сервера ===")
        print(result_text)
        
        speak("Скриншот успешно обработан!")
        speak(result_text[:500])
        
        break  # Закомментируй или убери этой строчку, если хочешь, чтобы он постоянно анализировал экран в цикле

    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Ошибка/Перегрузка: {e}. Повтор через 2 сек...")
        time.sleep(2)
