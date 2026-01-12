# 🍽️ FoodFit - Умный помощник для сочетаний продуктов и генерации рецептов

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/DRF-3.16.1-red.svg)](https://www.django-rest-framework.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**FoodFit** — это веб-приложение для подбора оптимальных сочетаний продуктов с генерацией рецептов через искусственный интеллект. Проект демонстрирует навыки fullstack-разработки на Python/Django.

## ✨ Возможности

- 🔍 **Умный поиск** ингредиентов с автодополнением
- 🤝 **Система рекомендаций** сочетаемости продуктов
- 🍳 **Разделение по типам** приготовления (для готовки / для подачи)
- 📊 **Отображение КБЖУ** и информации об аллергенах
- 🤖 **Генерация рецептов** с помощью YandexGPT AI
- 📱 **Адаптивный интерфейс** для любых устройств

## 🏗️ Технологический стек

**Backend:**
- Python 3.12
- Django 6.0
- Django REST Framework 3.16.1
- SQLite / PostgreSQL (production)
- Django Caching Framework

**Frontend:**
- Чистый JavaScript (ES6+)
- HTML5 + CSS3
- Fetch API для коммуникации
- Без использования фреймворков (vanilla JS)

**Инфраструктура:**
- Git для контроля версий
- dotenv для конфигурации
- requests для HTTP-запросов

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.10+
- pip (менеджер пакетов Python)
- Git

### Установка

1. **Клонирование репозитория:**
(используйте bash)

git clone https://github.com/GrosseLuchs/foodfit.git
cd foodfit

2. **Создание виртуального окружения:**

python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

3. **Установка зависимостей:**

pip install -r requirements.txt

4. **Настройка переменных окружения:**
Создайте файл .env в корне проекта с указанием следующих переменных:
SECRET_KEY=your-secret-key-here
YANDEX_API_KEY=your-yandex-api-key
YANDEX_FOLDER_ID=your-yandex-folder-id

5. **Миграции базы данных:**

python manage.py makemigrations
python manage.py migrate

6.  **Создание суперпользователя:**

python manage.py createsuperuser

7.  **Запуск сервера разработки:**

python manage.py runserver

Приложение будет доступно по адресу: http://localhost:8000

### Структура проекта:

foodfit_project/
├── backend/           # Основное приложение с моделями и бизнес-логикой
│   ├── models.py     # Модели данных (Ingredient, Category, Pairing, Allergen)
│   ├── utils.py      # Алгоритмы рекомендаций (оптимизированные)
│   └── admin.py      # Конфигурация админ-панели
├── api/              # REST API эндпоинты
│   ├── serializers.py # Сериализаторы DRF
│   └── views.py      # API представления
├── frontend/         # Пользовательский интерфейс
│   ├── templates/    # HTML шаблоны
│   └── views.py      # Контроллеры Django
├── services/         # Интеграции с внешними сервисами
│   ├── ai_integration.py  # Главный сервис AI
│   ├── yandex_gpt_client.py # Клиент YandexGPT
│   └── recipe_parser.py    # Парсер рецептов
└── foodfit_project/  # Настройки проекта
    ├── settings.py   # Основные настройки
    └── urls.py       # Маршруты URL

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
1. Возможность регистрации пользователейна платформе
2. Возможность добавления ингридиентов зарегистрированными пользователями
3. Возможность сохранять понравившийся рецепт зарегистрированным пользователям
4. Реализация рейтинга для рецептов
5. Возможность сохранения рецепта в нужном формате (txt, pdf, html)


## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

## 👏 Благодарности

- [Yandex Cloud](https://cloud.yandex.ru/) за предоставление GPT API
- Учебной программе [Яндекс.Практикум](https://practicum.yandex.ru/)

## 📞 Контакты

Александр Островский - [GitHub](https://github.com/GrosseLuchs) - ostrovsky.alexander@email.com

Проект: [https://github.com/GrosseLuchs/foodfit](https://github.com/GrosseLuchs/foodfit)
