FROM python:3.12

COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt --user

ENV TELEGRAM_KEY=
ENV GEMINI_KEY=
ENV BOT_USERNAME=
ENV BOT_PASSWORD=

CMD ["python3","bot.py"]

