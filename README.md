

## Дипломный проект: Foodgram
![workflow](https://github.com/DandyBoo/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

Онлайн-сервис, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на других авторов, а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Используемые технологии:
Python 3.7 
Django 3.2.18 
Docker Docker-compose
Postgresql
NGINX

### Проект развернут на сервере: [158.160.44.241](http://158.160.44.241/)

### Структура файла .env:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя_базы_данных>
POSTGRES_USER=<логин_для_подключения_к_БД>
POSTGRES_PASSWORD=<пароль_для_подключения_к_БД>
DB_HOST=<название_сервиса_БД>
DB_PORT=<порт_для_подключения_к_БД> 
SECRET_KEY=<Django secret key>
```
### Для запуска проекта в контейнерах перейдите в директорию /infra и выполните команду:
```
sudo docker compose up -d --build
```
### Выполните миграции, создайте суперпользователя и соберите статику
```
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py createsuperuser
sudo docker compose exec backend python manage.py collectstatic --no-input 
```
### Ресурсы проекта:
* http://localhost/ - главная страница сайта;
* http://localhost/admin/ - админ панель;
* http://localhost/api/ - API проекта
* http://localhost/api/docs/redoc.html - документация к API

### Автор:
#### Андрей Пономарев