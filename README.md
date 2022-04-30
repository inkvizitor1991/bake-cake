# Сервис BAKE-CAKE
Онлайн-магазин для создания индивидуальных тортов.

## Запуск

Для запуска сайта вам понадобится Python третьей версии.

Скачайте код с GitHub:

```sh
git clone https://github.com/inkvizitor1991/bake-cake
```

Создайте и активируйте виртуальное окружение:

```sh
cd bake-cake
python -m venv venv
source venv/bin/activate
```

Установите зависимости:

```sh
pip install -r requirements.txt
```

Создайте базу данных SQLite:

```sh
python3 manage.py migrate
```
Заполните базу данных тестовыми данными:
```sh
python manage.py loaddata initial_db_dummy_data
```
Запустите тестовую версию сервера:

```
python3 manage.py runserver
```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны несколько переменных:
- `DEBUG` — дебаг-режим. Поставьте `True`, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `YOOKASSA_ACCOUNT_ID` — id магазина для платежей [ЮKassa](https://yookassa.ru/).
- `YOOKASSA_SECRET_KEY` — секретный ключ магазина [ЮKassa](https://yookassa.ru/).

## Цели проекта

Код написан в учебных целях — для курса по Python и веб-разработке на сайте [Devman](https://dvmn.org).