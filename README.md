# FXWorld

https://fxworld.ru/

Иновационное приложение для трейдинга физических с любого устройства.\
Функциональность приложения включает:
- Онлайн котировки всех инструментов
- Подача заявок онлайн
- Продвинутый анализ котировок
- Прогнозирование цен на основе продвинутых ML-моделей
- Полезные подсказки прям в форме подаче заявок
- Удобный личный кабинет
- Возможность создания банковского счета прям из приложения


## Deployment
1. Склонировать репозиторий
1. Установить базу данных и прописать реквизиты подключения в файле настроек trapp_project/trapp/trapp.env.\
Пример содержания файла настроек (postgresql):

    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=db_name
    POSTGRES_USER=db_user
    POSTGRES_PASSWORD=db_password
    DB_HOST=127.0.0.1
    DB_PORT=5432
    
1. Находясь в директории trapp_project установить venv:

    python -m venv venv

1. Запустить venv:
    . venv/bin/activate (linux)
    source venv/Scripts/activate (winda)
    
1. Установить зависимости:

    pip install -r requirements.txt

1. Перейти в trapp_project/trapp и выполнить:

    python manage.py makemigrations
    python manage.py migrate    
    python manage.py runserver
    
После этого интерфейс приложения будет доступен по адресу http://127.0.0.1:8000

## Credentials
Made by Tolbanchiki Team (c), 2022. \
All rights reserved.
