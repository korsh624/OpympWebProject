Инструкция по запуску

1) Cоздайте виртуальное окружение
python -m venv venv

2) Активируйте виртуальное окружение
source venv/bin/activate

3) Установите зависимости
pip install -r requirements.txt

4) Перейдите в директорию с проектом
cd freelance

5) Проведите миграции базы данных
python manage.py makemigrations
python manage.py migrate

6) Создайте администратора (панель доступна по пути host.domain/admin)
python manage.py createsuperuser

7) Запустите проект
python manage.py runserver

8) Откройте веб сайт по пути 127.0.0.1:8000 или с любыми другими параметрами, которые Вы указали при старте веб сервера