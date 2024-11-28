from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot
from journal.models import Journal 

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)

class Command(BaseCommand):
    help = 'A command to launch the Telegram bot.'

    def handle(self, *args, **kwargs):
        @bot.message_handler(func=lambda message: message.text.startswith("!"))
        def handle_message(message):
            try:
                content = message.text[1:].strip()
                parts = content.split("*")
                
                if len(parts) == 2:
                    completed_work = parts[0].strip()  # До "*"
                    place_of_work = parts[1].strip()  # После "*"
                else:
                    bot.reply_to(message, "Ошибка: сообщение должно быть в формате `! Задание * Место`.")
                    return

                Journal.objects.create(
                    name=message.from_user.username or "Неизвестный", 
                    completed_work=completed_work,
                    place_of_work=place_of_work
                )
                bot.reply_to(message, "Запись добавлена успешно!")
            except Exception as e:
                bot.reply_to(message, f"Ошибка добавления записи: {e}")

        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.infinity_polling()
