FROM python:3.9

WORKDIR /chatbot

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./chatbot /chatbot

CMD ["python", "chatbot/chatbot.py"]
