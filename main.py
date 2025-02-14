import telebot
from telebot import types
import logging
import threading
import time
from datetime import datetime, timedelta
import random

logging.basicConfig(level=logging.INFO)

API_TOKEN = '7880925636:AAEBv-iQKTL6rgGq6Y3PDCtMm38FsMqX194'
bot = telebot.TeleBot(API_TOKEN)

users_data = {}
user_authentication = {}   

def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💸Добавить расход", "👀Посмотреть расходы")
    keyboard.add("📈Анализ расходов", "💰Установить бюджет")
    keyboard.add("👀Посмотреть бюджет", "💡Советы по финансовой грамотности")
    keyboard.add("⏰Добавить напоминание", "👀Посмотреть напоминания")
    keyboard.add("💲Перейти в копилку💲")
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

def add_expense(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        users_data[user_id]['expenses'].append(amount)
        bot.send_message(message.chat.id, f"Расход {amount} добавлен.")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())

    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
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
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму бюджета.")
        bot.register_next_step_handler(message, set_budget)


def financial_tips(message):
    all_tips = [
        "Создайте бюджет. Записывайте доходы и расходы, чтобы видеть, куда уходят деньги.",
        "Ставьте цели. Определите краткосрочные и долгосрочные финансовые цели.",
        "Экономьте 10% дохода. Отложите часть дохода на сбережения.",
        "Планируйте расходы. Ищите способы сократить ненужные траты.",
        "Изучайте кредиты. Понимание условий кредитования поможет избежать переплат.",
        "Следите за кредитной историей. Проверяйте свою кредитную историю на наличие ошибок.",
        "Инвестируйте. Начинайте инвестировать, даже если суммы небольшие.",
        "Создавайте резервный фонд. Накопите средства на 3-6 месяцев расходов.",
        "Изучайте финансовую литературу. Читайте книги и статьи о финансах.",
        "Будьте осторожны с кредитными картами. Используйте их разумно, чтобы избежать долгов.",
        "Используйте приложения для учета. Устанавливайте приложения для отслеживания финансов.",
        "Сравнивайте цены. Перед покупкой сравнивайте цены в разных магазинах.",
        "Избегайте импульсивных покупок. Дайте себе время подумать перед покупкой.",
        "Следите за скидками и акциями. Используйте скидки, чтобы сэкономить.",
        "Планируйте крупные покупки. Не делайте их внезапно, обдумайте бюджет.",
        "Учитесь на ошибках. Анализируйте свои финансовые решения и ошибки.",
        "Соблюдайте налоговые обязательства. Понимание налогов поможет избежать штрафов.",
        "Не забывайте про пенсионные накопления. Начинайте откладывать на пенсию как можно раньше.",
        "Учитывайте инфляцию. Это поможет вам рассчитывать на будущее.",
        "Делитесь знаниями. Обменивайтесь опытом с друзьями и близкими."
    ]
    
    # Случайным образом выбираем 5 уникальных советов
    selected_tips = random.sample(all_tips, k=min(5, len(all_tips)))
    
    # Формируем сообщение с советами, сохраняя порядок
    tips_msg = "\n".join([f"{i + 1}. {tip}" for i, tip in enumerate(selected_tips)])
    response_message = f"⬇️Вот тебе несколько советов по финансовой грамотности⬇️\n{tips_msg}"
    
    try:
        bot.send_message(message.chat.id, response_message)
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


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
        bot.send_message(message.chat.id, "❌Пожалуйста, введите время в корректном формате.")
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

    
def go_to_savings(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Вы в копилке. Выберите действие:", reply_markup=savings_menu_keyboard())

def savings_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💲Просмотреть копилку","➕Добавить средства в копилку")
    keyboard.add("📍Установить цель накоплений", "🗑️Сбросить копилку")
    keyboard.add("🔙Назад в главное меню")
    return keyboard

@bot.message_handler(func=lambda message: message.text == "💲Перейти в копилку💲")
def handle_go_to_savings(message):
    go_to_savings(message)

@bot.message_handler(func=lambda message: message.text == "💲Просмотреть копилку")
def handle_view_savings(message):
    user_id = message.from_user.id
    total_savings = users_data[user_id].get('savings', 0)
    target_savings = users_data[user_id].get('target_savings', 0)

    if target_savings > 0:
        progress = total_savings / target_savings * 100
        line_length = 20  # Длина линии прогресса
        filled_length = int(line_length * progress // 100)
        bar = '█' * filled_length + '-' * (line_length - filled_length)
        response = f"Ваша копилка:\n\nНакоплено: {total_savings} рублей\nЦель: {target_savings} рублей\nПрогресс: [{bar}] {progress:.2f}%"
    else:
        response = "❌Вы еще не начали копить."

    bot.send_message(message.chat.id, response, reply_markup=savings_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "➕Добавить средства в копилку")
def handle_add_to_savings(message):
    bot.send_message(message.chat.id, "Введите сумму для добавления в копилку:")
    bot.register_next_step_handler(message, save_to_savings)

def save_to_savings(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        users_data[user_id]['savings'] = users_data[user_id].get('savings', 0) + amount
        bot.send_message(message.chat.id, f"Вы успешно добавили {amount} рублей в копилку.")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=savings_menu_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, save_to_savings)

@bot.message_handler(func=lambda message: message.text == "📍Установить цель накоплений")
def handle_set_target_savings(message):
    bot.send_message(message.chat.id, "Сколько вы хотите накопить?")
    bot.register_next_step_handler(message, save_target_savings)

def save_target_savings(message):
    user_id = message.from_user.id
    try:
        target_amount = float(message.text)
        users_data[user_id]['target_savings'] = target_amount
        bot.send_message(message.chat.id, f"Цель накоплений установлена на уровне {target_amount} рублей.")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=savings_menu_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, save_target_savings)

@bot.message_handler(func=lambda message: message.text == "🔙Назад в главное меню")
def handle_back_to_main_menu(message):

    bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=main_menu_keyboard())


@bot.message_handler(func=lambda message: message.text == "💲Перейти в копилку💲")
def handle_go_to_savings(message):
    go_to_savings(message)

@bot.message_handler(func=lambda message: message.text == "🗑️Сбросить копилку")
def handle_reset_savings(message):
    user_id = message.from_user.id
    users_data[user_id]['savings'] = 0
    users_data[user_id]['target_savings'] = 0  # Сброс цели накоплений (опционально)
    bot.send_message(message.chat.id, "Копилка успешно сброшена.")
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=savings_menu_keyboard())


@bot.message_handler(func=lambda message: True)
def unknown_message(message):
    bot.send_message(message.chat.id, "Я не понимаю вас😔. Пожалуйста, выберите что-то из меню.")

if __name__ == '__main__':
bot.polling(none_stop=True)