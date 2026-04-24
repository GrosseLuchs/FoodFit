import logging
import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.conf import settings

logger = logging.getLogger('foodfit')


class YandexGPTClient:
    """Клиент для работы с Yandex GPT API"""

    def __init__(self):
        self.api_key = getattr(settings, 'YANDEX_API_KEY', '')
        self.folder_id = getattr(settings, 'YANDEX_FOLDER_ID', '')
        self.base_url = (
            "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        )
        self.session = self._create_session()

    def _create_session(self):
        """Создаёт сессию с повторными попытками при ошибках 5xx и таймаутах"""
        session = requests.Session()
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount('https://', adapter)
        session.mount('http://', adapter)
        return session

    def is_configured(self):
        """Проверяет, заданы ли API ключи"""
        return bool(self.api_key and self.folder_id)

    def generate_recipe(self, ingredient_names):
        """
        Генерирует рецепт через YandexGPT,
        возвращает ответ API или None при ошибке
        """
        if not self.is_configured():
            logger.warning("YandexGPT: отсутствуют API ключи")
            return None

        prompt = self._build_prompt(ingredient_names)
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.7,
                "maxTokens": 1000
            },
            "messages": [
                {
                    "role": "system",
                    "text": (
                        "Ты опытный повар. Отвечай только в формате JSON "
                        "на русском языке."
                    )
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }

        try:
            response = self.session.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=15
            )
            response.raise_for_status()
            logger.debug("YandexGPT API ответил успешно")
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Таймаут при запросе к YandexGPT (15 секунд)")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP при запросе к YandexGPT: {e}")
            return None

    def _build_prompt(self, ingredient_names):
        """Формирует промпт для YandexGPT"""
        ingredients_str = ', '.join(ingredient_names)
        return f"""
        Ты профессиональный шеф-повар.
        Создай практичный рецепт на основе ингредиентов: {ingredients_str}.

        Ответ дай в формате JSON:
        {{
            "title": "Название блюда",
            "time": "Время приготовления",
            "ingredients": [
                "ингредиент 1 с количеством",
                "ингредиент 2 с количеством"
            ],
            "instructions": "1. Шаг первый\\n2. Шаг второй\\n3. Шаг третий",
            "tips": "Полезные советы"
        }}

        Рецепт должен быть простым для домашнего приготовления.
        """
