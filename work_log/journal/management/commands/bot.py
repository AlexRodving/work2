from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from journal.models import Journal  # Импорт вашей модели

# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

# Название класса обязательно - "Command"
class Command(BaseCommand):
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        # Обработчик для всех текстовых сообщений
        @bot.message_handler(content_types=['text'])
        def handle_message(message):
            try:
                # Добавляем запись в таблицу Journal
                Journal.objects.create(
                    name=message.from_user.username or "Неизвестный",  # Имя пользователя
                    completed_work=message.text,  # Текст сообщения
                    place_of_work="Telegram Bot"  # Условное место выполнения
                )
                bot.reply_to(message, "Запись добавлена успешно!")
            except Exception as e:
                bot.reply_to(message, f"Ошибка добавления записи: {e}")

        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()  # Бесконечный цикл бота
