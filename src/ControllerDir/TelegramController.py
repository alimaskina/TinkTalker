from src.ModelDir.Model import Model
from src.ConfigDir.Config import Config
from src.ViewDir.VIEWs import ViewFactory
import telebot


class TelegramController:
    """Класс, контролирующий взаимодействие Представления (View) и Модели (Model)"""

    def __init__(self):
        self.__config = Config()
        self.__model = Model()
        self.__view = ViewFactory().create_view('telegram_bot')
        self.bot = telebot.TeleBot(self.__config.get_tg_token())

        # Контекст из последних 3 сообщений
        self.context = [' ', ' ', ' ']

    def run(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def hello(message):
            """Приветствие пользователя."""
            self.__view.hello(bot=self.bot, chat_id=message.chat.id)

        @self.bot.message_handler(content_types=['text'])
        def handle_message(message):
            """Обработка сообщений."""

            text = message.text
            self.context.append(text)
            self.context = self.context[1:]

            answer = self.__model.answer(self.context)
            self.context.append(answer)
            self.context = self.context[1:]

            self.__view.send_message(answer, bot=self.bot, chat_id=message.chat.id)

        self.bot.polling()
