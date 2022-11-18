git clone ...

Устанавливаем на компе postgres, создаем user, задаем пароль, grant all privileges, создаем db (у меня пароль, user, db - trapp)

в директории trapp_project/trapp/trapp создать файл .env, содержание:
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=trapp
    POSTGRES_USER=trapp
    POSTGRES_PASSWORD=trapp
    DB_HOST=127.0.0.1
    DB_PORT=5432
    
находясь в директории trapp_project установить venv:
    python -m venv venv

Запустить venv:
    . venv/bin/activate (linux)
    source venv/Scripts/activate (winda)
    
pip install > requirements.txt

переходим в trapp_project/trapp:
    python manage.py makemigrations
    python manage.py migrate (создает все таблицы в базе, таблицы надо будет заполнить конечно)
    
    python manage.py runserver (запускаем сервак)
    
    Переходим в браузер, набираем 127.0.0.1:8000 должна открыться стартовая страница


 
