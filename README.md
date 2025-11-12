<h1 align = "center">API-сервис для вопросов и ответов</h1>

<h3>Инстуркция по запуску: </h3>

Для запуска проекта необходимо перейти в папку, где находиться Dockerfile/docker-comsope файлы и прописать в консоль

```bash
docker-compose up --build
```

*если приложение не запускается, то это возможно связано с миграциями, для решения необходимо выполнить комманды:

```bash
docker-compose run --rm app alembic revision --autogenerate -m "Initial tables"
docker-compose run --rm app alembic upgrade head
```

<h3>Использование: </h3>

Для взаимодействия с API можно использовать swagger, который создаётся FastAPI. Для этого необходимо перейти по адрессу

```bash
http://127.0.0.1:8000/docs
```

И проверить работоспособность готового Backend приложения.

<h3>Тесты: </h3>

Также были реализованы unittest'ы для проекта, которые тестируют основной функционал:

```bash
qa_autotest.py - unittestы с "живой" БД

mock_aqa.py - моки тестирование функционала
```

Для запуска необходимо выполнить комманду:

```bash
python qa_autotest.py/mock_aqa.py
```

<h3>Swagger: </h3>

<img width="1309" height="729" alt="image" src="https://github.com/user-attachments/assets/dfb785ed-e0f6-48c0-bf9f-d8094125193b" />

<h3>Docker Dekstop: </h3>

<img width="1582" height="898" alt="image" src="https://github.com/user-attachments/assets/19db2b6f-fbaa-4f72-8a17-fdb53947d1b1" />

<h3>Каталоги:</h3>

1. migrations/ - каталог, в котором храняться миграции созданные при помощи alembic
2. models/ - каталог, в котором хранятиться код для создания скетела БД при помощи sqlalchemy
3. routers/ - каталог с API-эндопинтами
4. schemas/ - каталог с файлами, в котором храняться классы валидирующие данные
5. services/ - каталог с логикой обработки обращений к API-эндпоинтами

<h3>Используемый СТЭК: </h3>

1. Python
2. FastAPI
3. SQLAlchemy
4. Alembic
5. Pydantic
6. uvicorn
7. Docker
8. Unittest
9. requests
