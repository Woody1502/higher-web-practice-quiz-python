# Сервис для создания вопросов для викторин

---

API для сервиса с викторинами. При помощи этого API можно организовывать викторины (создавать, редактировать, удалять, обновлять)

---

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)

![Django REST](https://img.shields.io/badge/Django%20REST-ff1709?style=for-the-badge&logo=django&logoColor=white)


---

## Функционал

- CRUD для категорий, квизов и вопросов
- Вопросы можно найти по тексту
- Свой ответ можно проверить
- Поиск квиза по названию
- Получение рандомного вопроса
- Автотесты на pytest
- Админ панель с подсчетом количества вопросов по квизам и категориям
- Реализована Django команда для загрузки csv в БД

---

## Примеры запросов

### Получение списка категорий

**Метод и URL:**
```http
GET http://127.0.0.1:8000/api/category/
```



### Добавление категории

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/category/
```

**Тело запроса:**
```json
{
  "title": "string"
}
```

### Получение вопроса по тексту

**Метод и URL:**
```http
GET http://127.0.0.1:8000/api/question/by_text/python/
```

**Ответ:**
```json
[
  {
    "id": 1,
    "text": "Что такое Python?",
    "description": "Язык программирования",
    "options": [
      "Язык программирования",
      "Змея",
      "Фреймворк",
      "База данных"
    ],
    "correct_answer": "Язык программирования",
    "difficulty": "easy",
    "explanation": "Python — высокоуровневый язык программирования",
    "quiz_id": 1,
    "category_id": 1
  }
]
```
### Проверка ответа

**Метод и URL:**
```http
POST http://127.0.0.1:8000/api/question/2/check/
```

**Тело запроса:**
```json
{
  "correct_answer": "string"
}
```

### Получение квиза по названию

**Метод и URL:**
```http
GET http://127.0.0.1:8000/api/quiz/by_title/python/
```
**Ответ:**
```json
[
  {
    "id": 1,
    "title": "Основы Python",
    "description": "Вопросы о базовом синтаксисе и концепциях Python"
  }
]
```

### Получение рандомного вопроса

**Метод и URL:**
```http
GET http://127.0.0.1:8000/api/quiz/2/random_question/
```
**Ответ:**
```json
{
  "id": 6,
  "text": "Чему равно 2 + 2 * 2?",
  "description": "Порядок операций",
  "options": [
    "6",
    "8",
    "4",
    "10"
  ],
  "correct_answer": "6",
  "difficulty": "easy",
  "explanation": "Сначала выполняется умножение: 2*2=4, затем сложение: 2+4=6",
  "quiz_id": 2,
  "category_id": 2
}
```

---

## Как запустить проект

### Клонировать репозиторий

```bash
git clone https://github.com/Woody1502/higher-web-practice-quiz-python.git
cd /higher-web-practice-quiz-python
```

### Зависимости

```bash
uv sync
```


### Выполнить миграции

```bash
uv run python manage.py import_csv "путь"
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Запустить проект

```bash
uv run python manage.py runserver
```

---

## Авторы

Алексей Смолко (Программист)