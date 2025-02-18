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
    keyboard.add("👤Мой бюджет", "📊Мои расходы")
    keyboard.add("⏰Добавить напоминание", "👀Посмотреть напоминания")
    keyboard.add("💲Перейти в копилку💲")
    keyboard.add("💡Советы по финансовой грамотности")
    return keyboard

def budget_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💵Добавить средства в бюджет", "👀Посмотреть бюджет")
    keyboard.add("🔙Назад в главное меню")
    return keyboard

def expenses_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("💸Добавить расход", "👀Посмотреть расходы")
    keyboard.add("📈Анализ расходов", "🔙Назад в главное меню")
    return keyboard

def expense_selection_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("100", "200", "300", "400", "500")
    keyboard.add("🔢Ввести свою сумму")
    keyboard.add("🔙Назад")
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
    if user_id not in users_data:
        users_data[user_id] = {
            'budget': 0,
            'expenses': {},
        }
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Добро пожаловать в Личный финансовый бот! Выберите действие:", reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text in [
    "💡Советы по финансовой грамотности", "⏰Добавить напоминание", "👀Посмотреть напоминания", "👤Мой бюджет", "📊Мои расходы"])
def main_menu(message):
    user_id = message.from_user.id

    if message.text == "💡Советы по финансовой грамотности":
        financial_tips(message)

    elif message.text == "⏰Добавить напоминание":
        bot.send_message(message.chat.id, "Введите сумму платежа:")
        bot.register_next_step_handler(message, set_reminder_amount)
    
    elif message.text == "👀Посмотреть напоминания":
        view_reminders(message)

    elif message.text == "👤Мой бюджет":
        bot.send_message(message.chat.id, "Выберите действие с бюджетом:", reply_markup=budget_menu_keyboard())

    elif message.text == "📊Мои расходы":
        bot.send_message(message.chat.id, "Выберите действие с расходами:", reply_markup=expenses_menu_keyboard())

@bot.message_handler(func=lambda message: message.text in ["💵Добавить средства в бюджет", "👀Посмотреть бюджет"])
def budget_menu(message):
    user_id = message.from_user.id
    
    if message.text == "💵Добавить средства в бюджет":
        bot.send_message(message.chat.id, "Введите сумму для добавления в бюджет:")
        bot.register_next_step_handler(message, add_to_budget)

    elif message.text == "👀Посмотреть бюджет":
        budget = users_data[user_id]['budget']
        bot.send_message(message.chat.id, f"Ваш текущий бюджет: {budget}")



@bot.message_handler(func=lambda message: message.text == "💸Добавить расход")
def add_expense_menu(message):
    bot.send_message(message.chat.id, "Введите категорию расхода:")
    bot.register_next_step_handler(message, enter_expense_category)

def enter_expense_category(message):
    user_id = message.from_user.id
    category = message.text
    bot.send_message(message.chat.id, "Выберите сумму расхода:", reply_markup=expense_selection_keyboard())
    bot.set_state(user_id, category)



@bot.message_handler(func=lambda message: message.text in ["100", "200", "300", "400", "500"])
def add_expense_fixed(message):
    user_id = message.from_user.id
    expense_amount = float(message.text)
    category = bot.get_state(user_id)  # Получаем сохраненную категорию

    if category not in users_data[user_id]['expenses']:
        users_data[user_id]['expenses'][category] = []  # Создаем список для новой категории

    users_data[user_id]['expenses'][category].append(expense_amount)
    users_data[user_id]['budget'] -= expense_amount  # Вычитаем из бюджета
    bot.send_message(message.chat.id, f"Вы добавили расход: {expense_amount} в категорию '{category}'. Текущий бюджет: {users_data[user_id]['budget']}")
    
    # Очистка состояния
    bot.delete_state(user_id)
    
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=expenses_menu_keyboard())

@bot.message_handler(func=lambda message: message.text == "🔢Ввести свою сумму")
def enter_custom_expense(message):
    bot.send_message(message.chat.id, "Введите свою сумму расхода:")
    bot.register_next_step_handler(message, add_expense_fixed )

@bot.message_handler(func=lambda message: message.text in ["👀Посмотреть расходы", "📈Анализ расходов"])
def expenses_menu(message):
    user_id = message.from_user.id
    
    if message.text == "👀Посмотреть расходы":
        view_expenses(message)

    elif message.text == "📈Анализ расходов":
        analyze_expenses(message)

def add_to_budget(message):
    user_id = message.from_user.id
    try:
        amount = float(message.text)
        users_data[user_id]['budget'] += amount
        bot.send_message(message.chat.id, f"Вы добавили {amount} к вашему бюджету. Текущий бюджет: {users_data[user_id]['budget']}")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=budget_menu_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, add_to_budget)

def add_expense_custom(message):
    user_id = message.from_user.id
    try:
        expense_amount = float(message.text)
        users_data[user_id]['expenses'].append(expense_amount)
        users_data[user_id]['budget'] -= expense_amount  # Вычитаем из бюджета
        bot.send_message(message.chat.id, f"Вы добавили расход: {expense_amount}. Текущий бюджет: {users_data[user_id]['budget']}")
        bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=main_menu_keyboard())
    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, add_expense_custom)

def view_expenses(message):
    user_id = message.from_user.id
    expenses = users_data[user_id]['expenses']
    
    if expenses:
        view_message = "Ваши расходы по категориям:\n"
        
        for category, expense_list in expenses.items():
            category_total = sum(expense_list)
            view_message += f"{category}: {category_total} (Всего записей: {len(expense_list)})\n"
        
        bot.send_message(message.chat.id, view_message)
    else:
        bot.send_message(message.chat.id, "У вас нет записанных расходов.")


@bot.message_handler(func=lambda message: message.text == "📊Анализ расходов")
def analyze_expenses(message):
    user_id = message.from_user.id
    expenses = users_data[user_id]['expenses']
    
    if expenses:
        total_expenses = sum(sum(expense_list) for expense_list in expenses.values())
        average_expense = total_expenses / sum(len(expense_list) for expense_list in expenses.values())
        
        analysis_message = f"Общая сумма расходов: {total_expenses}\nСредняя сумма расхода: {average_expense}\n\nРасходы по категориям:\n"
        
        for category, expense_list in expenses.items():
            category_total = sum(expense_list)
            analysis_message += f"{category}: {category_total}\n"
        
        bot.send_message(message.chat.id, analysis_message)
    else:
        bot.send_message(message.chat.id, "У вас нет расходов для анализа.")



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


# Функция для установки суммы напоминания
def set_reminder_amount(message):
    user_id = message.from_user.id
    amount = message.text

    try:
        amount = float(amount)
        bot.send_message(message.chat.id, "Введите текст напоминания:")
        bot.register_next_step_handler(message, lambda msg: set_reminder_datetime(msg, amount))
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму.")
        bot.send_message(message.chat.id, "Введите сумму платежа:")
        bot.register_next_step_handler(message, set_reminder_amount)

# Функция для установки даты и времени напоминания
def set_reminder_datetime(message, amount):
    user_id = message.from_user.id
    reminder_text = message.text

    bot.send_message(message.chat.id, "Введите дату и время напоминания в формате 'ДД.ММ.ГГГГ ЧЧ:ММ':")
    bot.register_next_step_handler(message, lambda msg: add_reminder(msg, reminder_text, amount))

# Функция для добавления напоминания
def add_reminder(message, reminder_text, amount):
    user_id = message.from_user.id
    datetime_str = message.text
    
    try:
        # Пробуем распарсить дату и время
        reminder_datetime = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M')

        # Проверяем наличие списка напоминаний у пользователя
        if 'reminders' not in users_data[user_id]:
            users_data[user_id]['reminders'] = []  # Инициализируем список напоминаний

        # Добавляем напоминание в данные пользователя
        users_data[user_id]['reminders'].append({
            'time': reminder_datetime,
            'message': reminder_text,
            'amount': amount
        })
        
        bot.send_message(message.chat.id, f"Напоминание установлено на {reminder_datetime.strftime('%d.%m.%Y %H:%M')} о платеже '{reminder_text}' на сумму {amount}.")

    except ValueError:
        bot.send_message(message.chat.id, "Некорректный формат. Пожалуйста, попробуйте снова.")
        bot.send_message(message.chat.id, "Введите дату и время напоминания в формате 'ДД.ММ.ГГГГ ЧЧ:ММ':")
        bot.register_next_step_handler(message, lambda msg: add_reminder(msg, reminder_text, amount))

# Функция для просмотра напоминаний
def view_reminders(message):
    user_id = message.from_user.id
    reminders = users_data[user_id].get('reminders', [])
    
    if not reminders:
        bot.send_message(message.chat.id, "У вас нет активных напоминаний.")
    else:
        response = "Ваши напоминания:\n"
        for reminder in reminders:
            response += f"- {reminder['message']} на сумму {reminder['amount']} в {reminder['time'].strftime('%d.%m.%Y %H:%M')}\n"
        bot.send_message(message.chat.id, response)
    
def go_to_savings(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Вы в копилке. Выберите действие:", reply_markup=savings_menu_keyboard())

def savings_menu_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📍Начать копить","➕Добавить средства в копилку")
    keyboard.add("💲Просмотреть копилку", "🗑️Сбросить копилку")
    keyboard.add("🔙Назад в главное меню")
    return keyboard

@bot.message_handler(func=lambda message: message.text == "💲Перейти в копилку💲")
def handle_go_to_savings(message):
    go_to_savings(message)


@bot.message_handler(func=lambda message: message.text == "📍Начать копить")
def handle_set_target_savings(message):
    bot.send_message(message.chat.id, "Сколько вы хотите накопить?")
    bot.register_next_step_handler(message, save_target_savings)    
def save_target_savings(message):
    user_id = message.from_user.id
    try:
        target_amount = float(message.text)
        users_data[user_id]['target_savings'] = target_amount
        
        # Запрашиваем, на что будет потрачена эта сумма
        bot.send_message(message.chat.id, "На что вы хотите накопить? Пожалуйста, укажите цель:")
        bot.register_next_step_handler(message, save_target_description, target_amount)
    except ValueError:
        bot.send_message(message.chat.id, "❌Пожалуйста, введите корректную сумму.")
        bot.register_next_step_handler(message, save_target_savings)


@bot.message_handler(func=lambda message: message.text == "💲Просмотреть копилку")
def handle_view_savings(message):
    user_id = message.from_user.id
    total_savings = users_data[user_id].get('savings', 0)
    target_savings = users_data[user_id].get('target_savings', 0)
    target_description = users_data[user_id].get('target_description', "Не установлено")

    # Проверка достижения цели
    if total_savings >= target_savings and target_savings > 0:
        bot.send_message(message.chat.id, "🎉 Поздравляем! Вы достигли своей цели по накоплениям!")

    if target_savings > 0:
        progress = total_savings / target_savings * 100
        line_length = 20  # Длина линии прогресса
        filled_length = int(line_length * progress // 100)
        bar = '█' * filled_length + '-' * (line_length - filled_length)  # Линия прогресса

        response = (f"Ваша копилка:\n\n"
                    f"Накоплено: {total_savings} рублей\n"
                    f"Цель: {target_savings} рублей\n"
                    f"На что: {target_description}\n"
                    f"Прогресс: [{bar}] {progress:.2f}%")
    else:
        response = "❌Вы еще не начали копить."

    bot.send_message(message.chat.id, response, reply_markup=savings_menu_keyboard())

def save_target_description(message, target_amount):
    user_id = message.from_user.id
    target_description = message.text
    
    # Сохраняем описание цели в данных пользователя
    users_data[user_id]['target_description'] = target_description
    
    bot.send_message(message.chat.id, f"Цель накоплений установлена на уровне {target_amount} рублей.\n"
                                       f"Цель: {target_description}.")
    bot.send_message(message.chat.id, "Выберите следующее действие:", reply_markup=savings_menu_keyboard())


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