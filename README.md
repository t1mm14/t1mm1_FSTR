# ФСТР API для горных перевалов

## Описание проекта
Проект представляет собой REST API для работы с информацией о горных перевалах. API позволяет туристам добавлять информацию о пройденных перевалах и просматривать информацию о существующих.

## Технологии
- Python 3.x
- Django 5.1
- Django REST Framework
- PostgreSQL

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env в корневой директории проекта со следующими параметрами:
SECRET_KEY=ваш_секретный_ключ
PEREVAL_NAME=имя_базы_данных
FSTR_DB_USER=пользователь_бд
FSTR_DB_PASSWORD=пароль_бд
FSTR_DB_HOST=хост_бд
FSTR_DB_PORT=порт_бд

5. Выполните миграции:
```bash
python manage.py migrate
```

6. Запустите сервер:
```bash
python manage.py runserver
```

## API Endpoints

### Создание записи о перевале
- URL: `POST /api/pereval/create/`
- Пример запроса:
```json
{
    "beauty_title": "пер.",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "user": {
        "email": "example@mail.ru",
        "fam": "Иванов",
        "name": "Иван",
        "otc": "Иванович",
        "phone": "79991234567"
    },
    "coords": {
        "latitude": 45.3842,
        "longitude": 7.1525,
        "height": 1200
    },
    "level_winter": "",
    "level_summer": "1A",
    "level_autumn": "",
    "level_spring": "",
    "images": [
        {
            "data": "https://example.com/image1.jpg",
            "title": "Подъём"
        }
    ]
}
```

### Получение списка перевалов
- URL: `GET /api/perevals/`

### Получение информации о конкретном перевале
- URL: `GET /api/perevals/{id}/`

### Получение информации о перевале по ID
- URL: `GET /api/submitData/{id}/`
- Описание: Возвращает полную информацию о перевале, включая статус модерации

### Редактирование информации о перевале
- URL: `PATCH /api/submitData/{id}/`
- Описание: Позволяет редактировать информацию о перевале, если он находится в статусе "new"
- Ограничения: 
  - Нельзя изменять данные пользователя (ФИО, email, телефон)
  - Доступно только для записей в статусе "new"

  ### Получение списка перевалов по email пользователя
- URL: `GET /api/submitData/?user__email={email}`
- Описание: Возвращает список всех перевалов, добавленных пользователем с указанным email
- Пример запроса: `GET /api/submitData/?user__email=example@mail.ru`

### User (Пользователь)
- email (Email пользователя, уникальный)
- phone (Номер телефона)
- fam (Фамилия)
- name (Имя)
- otc (Отчество)

### Coords (Координаты)
- latitude (Широта)
- longitude (Долгота)
- height (Высота над уровнем моря)

### Pereval (Перевал)
- beauty_title (Тип местности)
- title (Название)
- other_titles (Альтернативные названия)
- connect (Соединение)
- status (Статус модерации)
- level_winter/spring/summer/autumn (Сложность для разных сезонов)

### Image (Изображения)
- data (URL изображения)
- title (Название изображения)
- pereval (Связь с перевалом)

## Статусы записей
- new (Новая запись)
- pending (На модерации)
- accepted (Принято)
- rejected (Отклонено)

## Коды состояния HTTP

- 200 OK: Успешное выполнение запроса
- 400 Bad Request: Ошибка в данных запроса
- 404 Not Found: Перевал не найден
- 500 Internal Server Error: Внутренняя ошибка сервера

## Лицензия
[Укажите вашу лицензию]