# Django Video Call Application

This web application allows users to create video call rooms and communicate in real-time using WebRTC.

## Features

- Create video call rooms
- Join existing rooms
- Real-time video and audio communication
- Video and audio stream management
- List of active participants
- User authentication

## Requirements

- Python 3.8+
- pip (Python package manager)
- Web browser with WebRTC support

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd video_call_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
venv\Scripts\activate     # for Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running

1. Start the development server:
```bash
python manage.py runserver
```

2. Open a browser and go to: http://localhost:8000

## Usage

1. Log in using your credentials
2. Create a new room or join an existing one
3. Allow access to your camera and microphone
4. Start communicating!

---

# Приложение для видеозвонков на Django

Это веб-приложение позволяет пользователям создавать комнаты для видеозвонков и общаться в реальном времени с использованием WebRTC.

## Функциональность

- Создание комнат для видеозвонков
- Присоединение к существующим комнатам
- Видео и аудио связь в реальном времени
- Управление видео и аудио потоками
- Список активных участников
- Аутентификация пользователей

## Требования

- Python 3.8+
- pip (менеджер пакетов Python)
- Веб-браузер с поддержкой WebRTC

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd video_call_project
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции базы данных:
```bash
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

## Запуск

1. Запустите сервер разработки:
```bash
python manage.py runserver
```

2. Откройте браузер и перейдите по адресу: http://localhost:8000

## Использование

1. Войдите в систему, используя свои учетные данные
2. Создайте новую комнату или присоединитесь к существующей
3. Разрешите доступ к камере и микрофону
4. Начните общение! 