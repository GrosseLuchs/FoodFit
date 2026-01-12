import requests
from django.conf import settings


class YandexGPTClient:
    """Клиент для работы с Yandex GPT API"""

    def __init__(self):
        self.api_key = getattr(settings, 'YANDEX_API_KEY', '')
        self.folder_id = getattr(settings, 'YANDEX_FOLDER_ID', '')
        self.base_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def is_configured(self):
        return bool(self.api_key and self.folder_id)

    def generate_recipe(self, ingredient_names):
        """Генерирует рецепт через Yandex GPT"""
        if not self.is_configured():
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
                    "text": "Ты опытный повар. Отвечай только в формате JSON на русском языке."
                },
                {
                    "role": "user",
                    "text": prompt
                }
            ]
        }

        try:
            response = requests.post(self.base_url, headers=headers, json=data, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"YandexGPT API error: {e}")
            return None

    def _build_prompt(self, ingredient_names):
        return f"""
        Ты профессиональный шеф-повар. Создай практичный рецепт на основе ингредиентов: {', '.join(ingredient_names)}.

        Ответ дай в формате JSON:
        {{
            "title": "Название блюда",
            "time": "Время приготовления",
            "ingredients": ["ингредиент с количеством"],
            "instructions": "1. Шаг первый\\n2. Шаг второй",
            "tips": "Полезные советы"
        }}

        Рецепт должен быть простым для домашнего приготовления.
        """
