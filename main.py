import telebot
import random
from datetime import datetime

# Токен вашего бота
TOKEN = '7368730334:AAH9xUG8G_Ro8mvV_fDQxd5ddkwjxHnBoeg'
bot = telebot.TeleBot(TOKEN)

# Полные списки имен
male_names = [
    "Авдей", "Авксентий", "Агапит", "Агафон", "Акакий", "Акиндин", "Александр", "Алексей", "Альберт", 
    "Анатолий", "Андрей", "Антон", "Аркадий", "Арсений", "Артём", "Артур", "Богдан", "Борис", 
    "Вадим", "Валентин", "Валерий", "Василий", "Виктор", "Владимир", "Владислав", "Вячеслав", 
    "Гавриил", "Геннадий", "Георгий", "Герман", "Григорий", "Даниил", "Дмитрий", "Евгений", 
    "Егор", "Иван", "Игорь", "Илья", "Кирилл", "Константин", "Максим", "Матвей", "Михаил", 
    "Никита", "Николай", "Олег", "Павел", "Пётр", "Роман", "Руслан", "Сергей", "Степан", 
    "Тимофей", "Фёдор", "Юрий"
]

female_names = [
    "Аврора", "Агафья", "Аглая", "Аделаида", "Александра", "Алина", "Алиса", "Алла", 
    "Анастасия", "Анна", "Антонина", "Валентина", "Валерия", "Варвара", "Василиса", "Вера", 
    "Вероника", "Галина", "Дарья", "Евгения", "Екатерина", "Елена", "Елизавета", "Зоя", 
    "Ирина", "Кира", "Ксения", "Лариса", "Лидия", "Любовь", "Маргарита", "Марина", "Мария", 
    "Надежда", "Наталья", "Ольга", "Полина", "Светлана", "София", "Татьяна", "Юлия", "Яна"
]

male_surnames = [
    "Иванов", "Петров", "Сидоров", "Федоров", "Васильев", "Кузнецов", "Новиков", "Смирнов", 
    "Попов", "Киселев", "Зайцев", "Беляев", "Морозов", "Волков", "Соловьев", "Егоров", 
    "Романов", "Александров", "Лебедев", "Григорьев", "Павлов", "Виноградов", "Богданов", 
    "Крылов", "Дмитриев", "Гаврилов", "Михайлов", "Чернов", "Поляков", "Жуков", "Савельев", 
    "Тарасов", "Борисов", "Фролов", "Карпов", "Шевченко", "Гончаров", "Мартынов", "Леонов"
]

female_surnames = [
    "Иванова", "Петрова", "Сидорова", "Федорова", "Васильева", "Кузнецова", "Новикова", 
    "Смирнова", "Попова", "Киселева", "Зайцева", "Беляева", "Морозова", "Волкова", 
    "Соловьева", "Егорова", "Романова", "Александрова", "Лебедева", "Григорьева", 
    "Павлова", "Виноградова", "Богданова", "Крылова", "Дмитриева", "Гаврилова", 
    "Михайлова", "Чернова", "Полякова", "Жукова", "Савельева", "Тарасова", 
    "Борисова", "Фролова", "Карпова", "Шевченко", "Гончарова", "Мартынова", "Леонова"
]

def generate_patronymic(name, gender):
    if gender == 'Парень':
        if name.endswith('й') or name.endswith('ь'):
            return name[:-1] + 'евич'
        else:
            return name + 'ович'
    else:
        if name.endswith('й') or name.endswith('ь'):
            return name[:-1] + 'евна'
        else:
            return name + 'овна'

def generate_birthdate():
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    
    # Выбираем век (19 или 20)
    century = random.choice(['19', '20'])
    
    if century == '19':
        year = random.randint(85, 99)
        full_year = f"19{year}"
    else:
        year = random.randint(0, 12)
        full_year = f"20{year:02d}"
    
    return f"{day:02d}.{month:02d}.{full_year}"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('/genperson')
    bot.reply_to(message, "Привет! Используй /genperson для генерации случайной личности.", reply_markup=markup)

@bot.message_handler(commands=['genperson'])
def send_gender_choice(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Парень', 'Девушка')
    bot.send_message(message.chat.id, "Выберите пол:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['Парень', 'Девушка'])
def generate_person(message):
    gender = message.text
    if gender == 'Парень':
        name = random.choice(male_names)
        surname = random.choice(male_surnames)
    else:
        name = random.choice(female_names)
        surname = random.choice(female_surnames)
    
    patronymic = generate_patronymic(random.choice(male_names), gender)
    birthdate = generate_birthdate()
    
    response = (
        "Генерируемая личность:\n"
        f"1. ФИО: {surname} {name} {patronymic}\n"
        f"2. Дата рождения: {birthdate}"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('/genperson')
    bot.send_message(message.chat.id, response, reply_markup=markup)

print("Бот запущен...")
bot.infinity_polling()
