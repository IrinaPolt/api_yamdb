## <h1 align="center"> Проект YaMDb </h1>


## Описание проекта

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
К проекту по адресу <http://127.0.0.1:8000/redoc/> подключена документация API YaMDb. В ней описаны возможные запросы к API и структура ожидаемых ответов. Для каждого запроса указаны уровни прав доступа: пользовательские роли, которым разрешён запрос.


### Разработчики
* [Ирина Полтарыхина](https://github.com/IrinaPolt)
* [Дарья Русинова](https://github.com/rusinovada)
* [Максим Фагин](https://github.com/imakswell)

## Инструкция по установке и запуску проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone https://github.com/IrinaPolt/api_yamdb.git
```

```bash
cd api_yamdb
```

2. Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```
Linux и MacOS:
```bash
source env/bin/activate
```
Windows:
```
source venv/Scripts/activate
```
3. Установить зависимости из файла requirements.txt:

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

4. Выполнить миграции:

```bash
python manage.py migrate
```

5. Запустить проект:

```bash
python manage.py runserver
```
## Системные требования

django==2.2.16
djangorestframework==3.12.4
requests==2.26.0
PyJWT==2.1.0
pytest==6.2.4
pytest-django==4.4.0
pytest-pythonpath==0.7.3
djangorestframework-simplejwt==5.2.0
django-filter==21.1
