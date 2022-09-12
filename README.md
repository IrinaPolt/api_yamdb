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

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv env
```
Linux и MacOS:
```bash
source env/bin/activate
```
Windows:
```
source env/Scripts/activate
```
Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Выполнить миграции:

```bash
python3 manage.py migrate
```

Запустить проект:

```bash
python3 manage.py runserver
```
