# Использование базового образа Python
FROM python:3.9-slim

# Устанавка рабочей директории в контейнере
WORKDIR /app

# Копируем содержимое текущей директории в рабочую директорию
COPY . /app

# Установка зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Загрузка переменных окружения из файла .env
ENV SPEECHKIT_API_KEY=${SK_TOKEN}

# Запуск приложения
CMD ["python", "app.py"]
