# Проект «Продуктовый помощник»
Дипломный проект - это сайт Foodgram, который является "Продуктовым помощником". На этом сайте пользователи могут делать следующие действия:

- Публиковать свои рецепты: Пользователи могут создавать и публиковать свои рецепты на сайте, чтобы поделиться ими с другими пользователями.
- Подписываться на публикации: Пользователи могут подписываться на других пользователей, чтобы получать уведомления о новых рецептах и публикациях.
- Добавлять рецепты в список "Избранное": Пользователи могут добавлять понравившиеся рецепты в свой список "Избранное", чтобы легко находить их в будущем.
- Скачивать сводный список продуктов: Пользователи могут скачивать сводный список продуктов, необходимых для приготовления выбранных блюд. Этот список поможет им с покупками перед походом в магазин.

Цель сайта Foodgram - помочь пользователям в планировании и приготовлении разнообразных блюд, а также облегчить процесс покупок продуктов.

## Проект запущен на сервере и доступен по адресу: 
- https://diploma.myftp.org/


### Для того чтоб запустить его на ВМ, нужно:
 Заполнение .env
*Шаблон env файла*
```
* EMAIL_HOST_PASSWORD= пароль от почты с которой будет отправляться код для подтверждения 
* EMAIL_HOST_USER= логин почты
* DB_ENGINE= испольщзуемая база данных
* DB_NAME= имя базы
* POSTGRES_USER= имя для захода в базу
* POSTGRES_PASSWORD= пароль от базы
* DB_HOST=db
* DB_PORT= порт
```
### Описание команд для запуска приложения в контейнерах
```
docker-compose up -d --build` - для того чтоб забилдить и контейнеры (без логов -d)
docker-compose exec backend python manage.py migrate (миграции)
docker-compose exec backend python manage.py createsuperuser (создание суперюзера)
docker-compose exec backend python manage.py collectstatic --no-input (сбор статических файлов)
```

### python + DRF + Djoser