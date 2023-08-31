import requests
from src.ConfigDir.Config import Config

from transformers import AutoTokenizer, AutoModelForCausalLM


class Model:
    """Класс, отвечающий за всю внутреннюю логику работы. """

    def __init__(self):
        self.__config = Config()
        self.url = self.__config.get_url()

    def answer(self, context):
        # Делаем запрос к модели
        data = {'context': context}
        response = requests.post(self.url, json=data)
        answer = response.content.decode("utf-8")
        
        return answer
    
