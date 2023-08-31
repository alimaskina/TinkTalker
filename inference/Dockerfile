FROM python:3.10

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY inference.py /code/
COPY model/ /code/model/
COPY tokenizer/ /code/tokenizer/

CMD ["uvicorn", "inference:app", "--host", "0.0.0.0", "--port", "8000"]