import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Замените на ваш API токен
API_TOKEN = '7368730334:AAH9xUG8G_Ro8mvV_fDQxd5ddkwjxHnBoeg'

bot = telebot.TeleBot(API_TOKEN)

# Функция для запуска Selenium и работы с сайтом
def process_site(user_text):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Открытие браузера в фоновом режиме
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        driver.get('https://www.dencode.com/en/cipher/caesar')  # Сайт для шифрования
        logger.info("Сайт загружен")
        
        # Ожидание и ввод текста в поле
        wait = WebDriverWait(driver, 10)
        input_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea#v')))
        input_field.clear()
        input_field.send_keys(user_text)
        logger.info(f"Введен текст: {user_text}")
        
        # Ожидание результата шифрования
        result_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span#encCipherCaesar')))
        result_text = result_field.text
        logger.info(f"Результат шифрования: {result_text}")
        
        return result_text

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        return None

    finally:
        driver.quit()

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите текст, который нужно зашифровать.")

# Обработка текста от пользователя
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_text = message.text
    result = process_site(user_text)
    
    if result:
        bot.reply_to(message, f"Результат шифрования: {result}")
    else:
        bot.reply_to(message, "Произошла ошибка при обработке текста. Попробуйте снова.")

bot.polling()
