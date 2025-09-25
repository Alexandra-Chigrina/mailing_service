# **Mailing Service**

## **Описание**:

Mailing Service — это веб-приложение для создания, управления и автоматической отправки email-рассылок с поддержкой
периодичности, логированием и возможностью отслеживания попыток доставки.

## **Установка**:

1. Клонируйте репозиторий

```
git@github.com:Alexandra-Chigrina/mailing_service.git
```

2. В терминале инициализируйте Poetry и активируйте виртуальное окружение

```
poetry init
poetry shell
```

Или, если используете venv:

```commandline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте .env на основе .env.example

4. Выполните миграции и создайте суперпользователя:

```commandline
python manage.py migrate
python manage.py createsuperuser
```
Панель администратора:
`http://127.0.0.1:8000/admin/`

## **Использование**:

### Запустите сервер и откройте сайт в браузере:.

```
python manage.py runserver
```

`http://127.0.0.1:8000/`

### Запуск планировщика рассылок:

```
python manage.py run_scheduler
```


### Функциональность

Рассылки: создание, редактирование, периодичность (none, daily, weekly, monthly)

Автоматическая отправка по расписанию: с использованием django-apscheduler

Попытки отправки: запись каждой попытки в MailingAttempt с логированием успехов/ошибок

Пользователи: регистрация, профиль, права доступа

Логирование: подробные логи записываются в logs/mailing.log


### Логирование

Файл логов: 'logs/mailing.log'

Конфигурация логов прописана в settings.py:

`
'handlers': {
    'mailing_file': {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'filename': os.path.join(BASE_DIR, 'logs', 'mailing.log'),
        'formatter': 'verbose',
    },
}
`

### Используемые технологии

- Python, Django

- PostgreSQL

- Redis (для кеширования)

- APScheduler

- Bootstrap (вёрстка)


## **Структура проекта**

mailing_service
├── mailing/                          # Приложение сервиса рассылок
│ ├── migrations/                     # Миграции базы данных Django
│ ├── templates/                      # Шаблоны HTML
│   ├── mailing/                      # Шаблоны, относящиеся к приложению mailing
│ ├── urls.py                         # Маршруты для mailing 
│ ├── admin.py                        # Настройка админки Django
│ ├── views.py                        # Контроллеры отображения страниц и обработки форм
│ ├── services.py                     # Бизнес-логика
│ ├── models.py                       # Модели: Client, Message, Mailing, MailingAttempt
│ ├── forms.py                        # Кастомные формы
│ ├── management/commands/            # Кастомные команды
│ ├── templatetags                    # Пользовательские шаблонные теги
│
├── users/                            # Приложение для управления пользователями
│ ├── templates/users/                # Шаблоны регистрации, логина, профиля
│ ├── forms.py                        # Формы для регистрации и профиля
│ ├── models.py                       # Кастомная модель пользователя
│ ├── views.py                        # Представления для регистрации, логина, профиля
│ ├── urls.py                         # Маршруты users
│
├── config/                           # Конфигурация проекта Django
│ ├── settings.py                     # Основные настройки проекта
│ ├── urls.py                         # Маршруты для всего проекта
│
├── media/                            # Медиафайлы, загруженные пользователями
│ ├── mailing/images.py 
│ ├── user/avatars .py
│
├── static/                           # Статические файлы (CSS, JS, изображения)
│ ├── css/                         
│ ├── bootstrap.min.css               # Bootstrap стилизация для шаблонов
│ ├── js/                           
│ ├── bootstrap.bundle.min.js         # Bootstrap функциональность #
│
├── logs/                             # Файл логов
│
├── manage.py                         # Управляющий файл Django-проекта
├── .venv                             # Виртуальное окружение
├── .gitignore                        # Исключения файлов из Git
├── .flake8                           # Настройки линтера Flake8
├── .poetry.lock                      # Фиксированные зависимости проекта  
├── .pyproject.toml                   # Основной конфигурационный файл проекта  
├── .env                              # Переменные окружения (не загружается в Git)
├── .env .sample                      # Шаблон .env
├── README.md                         # Документация  
