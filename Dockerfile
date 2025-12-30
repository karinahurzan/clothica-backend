FROM python:3.11-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності та оновлюємо pip
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту
COPY . .

# Використовуємо запуск через 'python -m', це надійніше, якщо шлях до бінарників збився
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]