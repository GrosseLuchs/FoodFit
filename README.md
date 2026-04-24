# 🍽️ FoodFit — Умный помощник для сочетания продуктов и генерации рецептов

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org)
[![CI](https://github.com/GrosseLuchs/FoodFit/actions/workflows/ci.yml/badge.svg)](https://github.com/GrosseLuchs/FoodFit/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**FoodFit** — веб-приложение для подбора оптимальных сочетаний продуктов и генерации рецептов с помощью YandexGPT.  
Проект демонстрирует навыки fullstack-разработки на Python/Django, работу с REST API, кэширование и CI/CD.

## ✨ Возможности

- 🔍 **Умный поиск** ингредиентов с автодополнением  
- 🤝 **Система рекомендаций** сочетаемости продуктов  
- 🍳 **Разделение по типам** (для готовки / для подачи)  
- 📊 **Отображение КБЖУ** и информации об аллергенах  
- 🤖 **Генерация рецептов** через YandexGPT  
- 📱 **Адаптивный интерфейс** для любых устройств  

## 🏗️ Технологический стек

**Backend:**  
- Python 3.12  
- Django 5.1  
- Django REST Framework 3.16.1  
- SQLite (разработка) / PostgreSQL (продакшн)  
- Django Caching Framework  

**Frontend:**  
- Чистый JavaScript (ES6+)  
- HTML5 + CSS3  
- Fetch API  
- Без сторонних фреймворков (vanilla JS)  

**Инфраструктура / DevOps:**  
- Git + GitHub Actions (CI)  
- pytest + pytest-django  
- flake8 (PEP8)  
- dotenv для конфигурации  
- requests для HTTP-запросов  

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.10+  
- pip  
- Git  

### Установка

1. **Клонирование репозитория**  
   ```bash
   git clone https://github.com/GrosseLuchs/foodfit.git
   cd foodfit/foodfit_project

2. **Создание виртуального окружения:**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   # или
   venv\Scripts\activate         # Windows

3. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt

4. **Настройка переменных окружения:**
Создайте файл .env в корне проекта с указанием следующих переменных:

   ```bash
   SECRET_KEY=ваш-секретный-ключ-django
   YANDEX_API_KEY=ваш-api-ключ-yandex-gpt
   YANDEX_FOLDER_ID=ваш-folder-id
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Миграции базы данных:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6.  **Создание суперпользователя:**
   ```bash
   python manage.py createsuperuser
   ```

7.  **Запуск сервера разработки:**
   ```bash
   python manage.py runserver
   ```

Приложение будет доступно по адресу: http://localhost:8000

### База данных

По умолчанию проект использует **SQLite** (файл `db.sqlite3`). Это удобно для локального запуска без дополнительной настройки
и демонстрации работы функционала.

Если вы хотите использовать **PostgreSQL** (например, для продакшена или тестирования), выполните следующие шаги:

1. Установите PostgreSQL и создайте базу данных.

2. Установите переменную окружения `DATABASE_URL`:

   ```bash
   DATABASE_URL=postgres://user:password@localhost:5432/foodfit
   ```

3. Установите расширение unaccent в PostgreSQL:

   ```sql
   CREATE EXTENSION IF NOT EXISTS unaccent;
   ```

4. Выполните миграции:
   ```bash
   python manage.py migrate
   ```

## 🧪 Тестирование

1. Для запуска тестов используйте pytest:

   ```bash
   pytest
   ```

2. Для проверки стиля кода (flake8):

   ```bash
   flake8 .
   ```

### Структура проекта:

foodfit_project/                # Корень проекта
├── backend/                    # Модели и бизнес-логика
│   ├── models.py               # Ingredient, Category, Allergen, Pairing
│   ├── utils.py                # Алгоритмы рекомендаций
│   └── admin.py                # Настройка админ-панели
├── api/                        # REST API
│   ├── serializers.py          # Сериализаторы DRF
│   └── views.py                # API-эндпоинты
├── frontend/                   # Пользовательский интерфейс
│   ├── templates/              # HTML-шаблоны
│   └── views.py                # Контроллеры Django
├── services/                   # Интеграция с внешними сервисами
│   ├── ai_integration.py       # Главный AI-сервис
│   ├── yandex_gpt_client.py    # Клиент YandexGPT
│   └── recipe_parser.py        # Парсер ответов GPT
├── foodfit_project/            # Настройки проекта
│   ├── settings.py
│   └── urls.py
├── tests/                      # Тесты (pytest)
│   ├── test_models.py
│   ├── test_api.py
│   ├── test_utils.py
│   └── conftest.py
├── .github/workflows/          # CI/CD (GitHub Actions)
├── .flake8                     # Конфигурация flake8
├── pytest.ini                  # Настройки pytest
├── requirements.txt
└── manage.py

## ⚡ Оптимизации производительности

- **Алгоритмы**: Оптимизированы с O(n²) до O(n) 
- **Кэширование**: Результаты рекомендаций кэшируются на 5 минут
- **База данных**: Индексы на ключевых полях для быстрого поиска
- **Запросы**: Используются select_related для минимизации запросов к БД
- **Фронтенд**: Debounce (300мс) для поиска уменьшает нагрузку
- **Безопасность**: Защита от XSS через DOM API вместо innerHTML

### 🔧 Использование
1. Для пользователей:

- Откройте главную страницу

- Введите название продукта в поисковой строке

- Выберите ингредиенты из результатов поиска

- Наблюдайте рекомендации по сочетаемости

- Нажмите "✨ Сгенерировать рецепт" для получения AI-рецепта

2. Для администраторов:

- Доступна админ-панель Django по адресу /admin:

- Управление ингредиентами и категориями

- Настройка сочетаний продуктов

- Модерация пользовательского контента

### Планы на будущее:
1. Возможность регистрации пользователей на платформе
2. Возможность добавления ингредиентов зарегистрированными пользователями
3. Возможность сохранять понравившийся рецепт зарегистрированным пользователям
4. Реализация рейтинга для рецептов
5. Возможность сохранения рецепта в нужном формате (txt, pdf, html)


## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## 👏 Благодарности

- [Yandex Cloud](https://cloud.yandex.ru/) за предоставление GPT API
- Учебной программе [Яндекс.Практикум](https://practicum.yandex.ru/)

## 📞 Контакты

Александр Островский - [GitHub](https://github.com/GrosseLuchs) - ostrovskii.alexandr@gmail.com

Проект: [https://github.com/GrosseLuchs/foodfit](https://github.com/GrosseLuchs/foodfit)
