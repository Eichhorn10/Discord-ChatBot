FROM python:3.10
WORKDIR /chatbot
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
COPY . .
COPY .env .
CMD ["python", "src/bot.py"]