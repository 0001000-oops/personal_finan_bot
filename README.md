# 💸Личный Финансовый бот @yourFinanc_bot

## Описание

[Личный финансовый бот](https://t.me/yourFinanc_bot) — это бот созданный с помощью библиотеки pyTelegramBotAPI, предназначенный для помощи пользователям в организации своих финансов. Он позволяет отслеживать расходы и доходы, устанавливать цели накоплений, устанавливать напоминание о платеже, добавлять средства в копилку и получать отчеты о финансовом состоянии.

## Функциональные возможности

После запуска бота вы увидите главное меню с доступными командами. Ниже приведены примеры использования каждой команды:

### 👤Мой бюджет

- **💵Добавить средства в бюджет**: Позволяет пользователю вводить сумму, которую он хочет добавить в свой бюджет.
*Пример использования:* Пользователь нажимает кнопку и вводит "500". Бот добавляет 500 рублей в бюджет и подтверждает действие сообщением: "Вы добавили 1000 к вашему бюджету. Текущий бюджет: 1000"

- **👀Посмотреть бюджет**: Отображает текущую сумму в бюджете.
*Пример использования:* Пользователь нажимает кнопку и получает сообщение с текущей суммой в бюджете (например, "Ваш бюджет: 1500 рублей").

### 📊Мои расходы

- **💸Добавить расход**: Пользователь может ввести сумму и описание расхода.
*Пример использования:* Пользователь нажимает кнопку, вводит категорию расхода "продукты", затем вводит сумму (или выбирает предложенную ботом) расхода "500" и бот добавляет этот расход в систему с сообщением: "Вы добавили расход: 500 в категорию 'продукты'. Текущий бюджет: 500"

- **👀Посмотреть расход**: Показывает список всех расходов пользователя.
*Пример использования:* Пользователь нажимает кнопку и получает список расходов, например:
       
      Общая сумма расходов: 1160.0
      Средняя сумма расхода: 415.0

       
- **📈Анализ расходов**: Предоставляет общий анализ расходов за определенный период.
*Пример использования:* Пользователь нажимает кнопку и получает отчет о расходах по категориям (например, "Еда: 500 рублей, Транспорт: 300 рублей").

### ⏰Добавить напоминание: Позволяет установить напоминание о предстоящем платеже.
*Пример использования:* Пользователь вводит "Напоминание о платеже 1000 рублей 15.02.2025", и бот отправит уведомление в указанное время с сообщением: "Напоминание: оплата за учебу на сумму 10.0"
### 👀Посмотреть напоминания: Показывает все активные напоминания.
*Пример использования:* Пользователь нажимает кнопку и получает список активных напоминаний, например:
     
     Ваши напоминания:
    - оплата за учебу на сумму 10.0 в 18.02.2025 06:15
     

### 💲Перейти в копилку💲

- **💲Просмотреть копилку**: Отображает текущее состояние накоплений пользователя.
*Пример использования:* Пользователь нажимает кнопку и видит сообщение "В вашей копилке: 2000 рублей."

- **➕Добавить средства в копилку**: Позволяет пользователю добавить деньги в копилку.
*Пример использования:* Пользователь вводит "Добавить 300 рублей", и бот обновляет сумму в копилке с сообщением: "Вы добавили 300 рублей в вашу копилку."

- **📍Установить цель накоплений**: Пользователь может установить конкретную цель накоплений.
*Пример использования:* Пользователь вводит "Собрать 5000 рублей на отпуск", и бот фиксирует эту цель с сообщением: "Цель накоплений установлена: 5000 рублей на отпуск."

- **🗑️Сбросить копилку**: Удаляет все данные о накоплениях и сбрасывает копилку к нулю.
*Пример использования:* Пользователь подтверждает действие, и бот сбрасывает копилку с сообщением: "Копилка сброшена."

## Установка

### Требования

- Python 3.x
- Библиотека pyTelegramBotAPI

### Установка зависимостей

Сначала клонируйте репозиторий.
В терминале введите:
- git clone https://github.com/yourusername/personal_finan_bot.git
- cd personal_finan_bot

Установите необходимые зависимости:
- pip install pyTelegramBotAPI 

### Настройка

1. Создайте бота в Telegram с помощью [BotFather](https://t.me/botfather) и получите токен.
2. В файле 'main.py' добавьте ваш токен:

- TOKEN = 'ВАШ_ТОКЕН'

## Запуск

Запустите бота:

- python main.py

## Лицензия

Этот проект лицензирован под MIT License - смотрите файл [LICENSE](LICENSE) для подробной информации.

---

Теперь вы можете начать взаимодействовать с ботом в Telegram! Спасибо за использование @yourFinanc_bot, надеюсь он поможет вам в организации ваших финансов!



