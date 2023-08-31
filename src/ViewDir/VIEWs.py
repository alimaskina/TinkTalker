import abc
from src.ConfigDir.Config import Config


class ViewFactory:
    """Этот класс создает объкты View."""

    def create_view(self, view_type):
        """Возвращает объект View заданного типа."""

        if view_type == 'telegram_bot':
            return TelegramView()
        else:
            raise ValueError(f'Unsupported view type: {view_type}')


class View(metaclass=abc.ABCMeta):
    """Интерефейс для обхектов View."""

    @abc.abstractmethod
    def hello(self, **kwargs):
        """Приветсвует пользователя и приглашет к беседе."""
        pass

    @abc.abstractmethod
    def send_message(self, data, **kwargs):
        """Отправляет сообщения."""
        pass


class TelegramView(View):
    """Этот объект может работать с Телеграмом."""

    def __init__(self):
        self.__config = Config()

    def hello(self, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']

        text = "Привет! Я буду рад поболтать с тобой. "
        bot.send_message(chat_id, text)

    def send_message(self, data, **kwargs):
        bot = kwargs['bot']
        chat_id = kwargs['chat_id']
        bot.send_message(chat_id, data)
