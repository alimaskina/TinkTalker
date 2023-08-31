from src.ConfigDir.Config import Config

from transformers import AutoTokenizer, AutoModelForCausalLM


class Model:
    """Класс, отвечающий за всю внутреннюю логику работы. """

    def __init__(self):
        self.__config = Config()
        self.tokenizer = AutoTokenizer.from_pretrained('../my_tg_token_1')
        self.model = AutoModelForCausalLM.from_pretrained('../my_tg_model_1')

    def answer(self, context):
        # Форматируем запрос
        context = [' '] * (3 - len(context)) + context
        text = f'@@ПЕРВЫЙ@@ {context[0]} @@ВТОРОЙ@@ {context[1]} @@ПЕРВЫЙ@@ {context[2]} @@ВТОРОЙ@@ '

        # Делаем запрос к модели
        inputs = self.tokenizer(text, return_tensors='pt')
        generated_token_ids = self.model.generate(
            **inputs,
            top_k=10,
            top_p=0.95,
            num_beams=3,
            num_return_sequences=3,
            do_sample=True,
            no_repeat_ngram_size=2,
            temperature=1.2,
            repetition_penalty=1.2,
            length_penalty=1.0,
            eos_token_id=50257,
            max_new_tokens=40
        )

        # Декодируем response и вытаскиваем сам ответ на сообщение
        context_with_response = [self.tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
        response = context_with_response[0].split("@@")[8]

        return response
