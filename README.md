# FXWorld
https://fxworld.ru/

### Приложение для трейдинга. Имитирует торговлю на бирже
(web адаптированный под mobile phone)

![alt text](https://github.com/timredz/trapp_project/blob/03833dcf32763ff55a016ea099f97752843c96da/fxworld_promo.png)

Данные идут онлайн от Биржи

#### Функциональность приложения включает:

Онлайн котировки валютных инструментов, достуна инфа по OrderBook
График цен (candles)
Подача заявок онлайн
Полезные подсказки прям в форме подаче заявок
Прогнозирование цен на основе продвинутых ML-моделей

#### Deployment
Склонировать репозиторий

Установить базу данных и прописать реквизиты подключения в файле настроек trapp_project/trapp/trapp.env.
Пример содержания файла настроек (postgresql):

DB_ENGINE=django.db.backends.postgresql DB_NAME=db_name POSTGRES_USER=db_user POSTGRES_PASSWORD=db_password DB_HOST=127.0.0.1 DB_PORT=5432

Находясь в директории trapp_project установить venv:

python -m venv venv

Запустить venv: . venv/bin/activate (linux) source venv/Scripts/activate (winda)

Установить зависимости:

pip install -r requirements.txt

Перейти в trapp_project/trapp и выполнить:

python manage.py makemigrations 
python manage.py migrate

cd marketdata/workers
python upload_mdata.py //загрузка пакета торговых данных (так как у вас нет marketdata feed)

python manage.py runserver

После этого интерфейс приложения будет доступен по адресу http://127.0.0.1:8000

Credentials
Made by Tolbanchiki Team (c), 2022.
All rights reserved.
