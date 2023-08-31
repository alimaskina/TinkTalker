from fastapi import FastAPI
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel

app = FastAPI()

class Model:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('tokenizer')
        self.model = AutoModelForCausalLM.from_pretrained('model')

    def answer(self, context):
        context = [' '] * (3 - len(context)) + context
        text = f'@@ПЕРВЫЙ@@ {context[0]} @@ВТОРОЙ@@ {context[1]} @@ПЕРВЫЙ@@ {context[2]} @@ВТОРОЙ@@ '
        inputs = self.tokenizer(text, return_tensors='pt')
        generated_token_ids = self.model.generate(
            **inputs,
            top_k=10,
            top_p=0.95,
            num_beams=3,
            num_return_sequences=1,
            do_sample=True,
            no_repeat_ngram_size=2,
            temperature=1.2,
            repetition_penalty=1.2,
            length_penalty=1.0,
            eos_token_id=50257,
            max_new_tokens=40
        )
        context_with_response = [self.tokenizer.decode(sample_token_ids) for sample_token_ids in generated_token_ids]
        response = context_with_response[0].split("@@")[8]
        return response


class RequestModel(BaseModel):
    context: list[str]


model = Model()


@app.post("/answer")
async def get_answer(request_model: RequestModel):
    return model.answer(request_model.context)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
