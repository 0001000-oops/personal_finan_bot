import telebot
from telebot import types
import logging
import threading
import time
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)


API_TOKEN = '7880925636:AAEBv-iQKTL6rgGq6Y3PDCtMm38FsMqX194'
bot = telebot.TeleBot(API_TOKEN)

users_data = {}


def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💸Добавить расход", "👀Посмотреть расходы")
    keyboard.add("📈Анализ расходов", "💰Установить бюджет")
    keyboard.add("👀Посмотреть бюджет", "💡Советы по финансовой грамотности")
    keyboard.add("⏰Добавить напоминание", "👀Посмотреть напоминания")
    return keyboard

def reminder_checker():
    while True:
        current_time = datetime.now()
        for user_id, data in users_data.items():
            reminders = data.get('reminders', [])
            for reminder in reminders:
                if reminder['time'] <= current_time:
                    bot.send_message(user_id, f"Напоминание: {reminder['message']} на сумму {reminder['amount']}")
                    reminders.remove(reminder)  # Удаляем напоминание после отправки
        time.sleep(60)  # Проверяем каждую минуту

# Запускаем поток для проверки напоминаний
threading.Thread(target=reminder_checker, daemon=True).start()




@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users_data.setdefault(user_id, {'expenses': [], 'budget': 0})
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Добро пожаловать в Личный финансовый бот! Выберите действие:", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text in ["💸Добавить расход", "👀Посмотреть расходы", "📈Анализ расходов",
 "💰Установить бюджет", "👀Посмотреть бюджет", "💡Советы по финансовой грамотности","⏰Добавить напоминание",
 "👀Посмотреть напоминания"])
def main_menu(message):
    user_id = message.from_user.id
    
    if message.text == "💸Добавить расход":
        bot.send_message(message.chat.id, "Введите сумму расхода:")
        bot.register_next_step_handler(message, add_expense)

    elif message.text == "👀Посмотреть расходы":
        view_expenses(message)

    elif message.text == "📈Анализ расходов":
        analyze_expenses(message)

    elif message.text == "💰Установить бюджет":
        bot.send_message(message.chat.id, "Введите ваш бюджет:")
        bot.register_next_step_handler(message, set_budget)

    elif message.text == "👀Посмотреть бюджет":
        budget = users_data[user_id]['budget']
        bot.send_message(message.chat.id, f"Ваш текущий бюджет: {budget}")

    elif message.text == "💡Советы по финансовой грамотности":
        financial_tips(message)

    elif message.text == "⏰Добавить напоминание":
        bot.send_message(message.chat.id, "Введите сумму платежа:")
        bot.register_next_step_handler(message, set_reminder_amount)

    elif message.text == "👀Посмотреть напоминания":
        view_reminders(message)


    elif message.text == "❌Выход":
        bot.send_message(message.chat.id, "Вы вышли из бота. До свидания!")





def add_expense(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        users_data[user_id]['expenses'].append(amount)
        bot.send_message(message.chat.id, f"Расход {amount} добавлен.")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, add_expense)


def view_expenses(message):
    user_id = message.from_user.id
    expenses = users_data[user_id]['expenses']
    
    if expenses:
        response = "\n".join(f"Расход: {exp}" for exp in expenses)
        bot.send_message(message.chat.id, f"Ваши расходы:\n{response}")
    else:
        bot.send_message(message.chat.id, "У вас пока нет расходов.")
    
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())

def analyze_expenses(message):
    user_id = message.from_user.id
    expenses = users_data[user_id]['expenses']
    
    if expenses:
        total_expenses = sum(expenses)
        average_expense = total_expenses / len(expenses)
        max_expense = max(expenses)
        min_expense = min(expenses)
        
        analysis_msg = (
            f"Общие расходы: {total_expenses}\n"
            f"Средний расход: {average_expense}\n"
            f"Максимальный расход: {max_expense}\n"
            f"Минимальный расход: {min_expense}"
        )
        
        bot.send_message(message.chat.id, analysis_msg)
    else:
        bot.send_message(message.chat.id, "У вас пока нет расходов для анализа.")
    
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())


def set_budget(message):
    user_id = message.from_user.id
    try:
        budget = float(message.text)
        users_data[user_id]['budget'] = budget
        bot.send_message(message.chat.id, f"Ваш бюджет установлен на сумму: {budget}")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму бюджета.")
        bot.register_next_step_handler(message, set_budget)


def financial_tips(message):
    tips = [
        "1. Создайте бюджет и придерживайтесь его.",
        "2. Старайтесь откладывать часть дохода на сбережения.",
        "3. Избегайте импульсивных покупок.",
        "4. Изучайте свои расходы и ищите способы их сократить.",
        "5. Инвестируйте в свое образование и навыки."
    ]
    
    tips_msg = "\n".join(tips)
    bot.send_message(message.chat.id, f"Советы по финансовой грамотности:\n{tips_msg}")
    
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())


def set_reminder_amount(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        users_data[user_id].setdefault('reminders', [])
        
        bot.send_message(message.chat.id, "Введите сообщение для напоминания:")
        bot.register_next_step_handler(message, lambda msg: set_reminder_time(msg, amount))
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, set_reminder_amount)

def set_reminder_time(message, amount):
    user_id = message.from_user.id
    reminder_message = message.text

    bot.send_message(message.chat.id, "Введите время для напоминания в формате ГГГГ-ММ-ДД ЧЧ:ММ (например, 2023-10-30 15:30):")
    bot.register_next_step_handler(message, lambda msg: add_reminder(msg, amount, reminder_message))

def add_reminder(message, amount, reminder_message):
    user_id = message.from_user.id
    
    try:
        reminder_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        users_data[user_id]['reminders'].append({'time': reminder_time, 'amount': amount, 'message': reminder_message})
        bot.send_message(message.chat.id, f"Напоминание добавлено на {reminder_time} о платеже {amount}.")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())
        
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите время в корректном формате.")
        bot.register_next_step_handler(message, lambda msg: add_reminder(msg, amount, reminder_message))

# Просмотр напоминаний
def view_reminders(message):
    user_id = message.from_user.id
    reminders = users_data[user_id].get('reminders', [])
    
    if reminders:
        response = "\n".join(f"{reminder['time']}: {reminder['message']} на сумму {reminder['amount']}" for reminder in reminders)
        bot.send_message(message.chat.id, f"Ваши напоминания:\n{response}")
    else:
        bot.send_message(message.chat.id, "У вас пока нет напоминаний.")
    
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())

bot.polling(none_stop=True)