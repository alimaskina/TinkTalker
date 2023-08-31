import os
from yaml import load, FullLoader
from dotenv import load_dotenv, find_dotenv


class Config:
    """Класс, отвечающий за настройки. Это синглтон."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            with open(os.path.dirname(os.path.abspath(__file__)) + '/config.yml', 'r') as f:
                config = load(f, Loader=FullLoader)
            cls._instance = super().__new__(cls)
            cls._instance.__dict__ = config

            load_dotenv(find_dotenv())
            cls._instance.__tgtoken__ = os.getenv('TG_TOKEN')

        return cls._instance

    def get_tg_token(self):
        """Геттер токена для телеграмм бота."""
        return self._instance.__tgtoken__

    def get_url(self):
        """Геттер url для модели."""
        return self._instance.__dict__['URL']
