import json
import re
import logging

logger = logging.getLogger('foodfit')


def parse_recipe_from_response(api_response, ingredient_names):
    """Парсит рецепт из ответа API YandexGPT"""
    if not api_response or 'result' not in api_response:
        logger.warning("Неверный ответ API: отсутствует поле 'result'")
        return None

    try:
        text = api_response['result']['alternatives'][0]['message']['text']
        text = _clean_response_text(text)

        try:
            recipe = json.loads(text)
        except json.JSONDecodeError:
            logger.debug(
                "Ответ не является чистым JSON, пробуем извлечь JSON из текста"
            )
            recipe = _extract_json_from_text(text)

        if not recipe:
            logger.warning("Не удалось извлечь JSON из ответа")
            return None

        return _validate_recipe(recipe, ingredient_names)

    except (KeyError, IndexError, TypeError) as e:
        logger.error(f"Ошибка при парсинге структуры ответа: {e}")
        return None
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при парсинге: {e}")
        return None


def _clean_response_text(text):
    """Очищает текст ответа от маркеров кода"""
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    return text.strip()


def _extract_json_from_text(text):
    """Извлекает JSON из текста с помощью регулярного выражения"""
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        else:
            logger.debug("JSON не найден в тексте")
            return None
    except json.JSONDecodeError:
        logger.debug("Найденная строка не является валидным JSON")
        return None
    except Exception as e:
        logger.error(f"Ошибка при извлечении JSON: {e}")
        return None


def _validate_recipe(recipe, ingredient_names):
    """Валидирует и дополняет рецепт, приводит все поля в нужный формат"""
    required_fields = ['title', 'time', 'ingredients', 'instructions', 'tips']
    for field in required_fields:
        if field not in recipe:
            recipe[field] = ""

    if not recipe['title']:
        first = ingredient_names[0] if ingredient_names else 'ингредиентов'
        recipe['title'] = f"Блюдо из {first}"

    if not recipe['time']:
        recipe['time'] = "30 минут"

    recipe['ingredients'] = _normalize_ingredients(
        recipe.get('ingredients'), ingredient_names
    )

    if not recipe['instructions']:
        recipe['instructions'] = (
            "1. Подготовьте ингредиенты.\n"
            "2. Приготовьте по своему вкусу.\n"
            "3. Подавайте!"
        )

    if not recipe['tips']:
        recipe['tips'] = "Подавайте горячим для лучшего вкуса."

    return recipe


def _normalize_ingredients(ingredients_data, fallback_ingredient_names):
    """
    Приводит поле 'ingredients' к единому формату: список строк.
    Поддерживает:
      - список строк
      - список словарей {'имя': 'количество'}
      - словарь {'имя': 'количество'}
      - строку с разделителями (например, через запятую)
    """
    if not ingredients_data:
        return [
            f"{name} - по вкусу" for name in fallback_ingredient_names
        ]

    if isinstance(ingredients_data, list):
        normalized = []
        for item in ingredients_data:
            if isinstance(item, dict):
                for ing_name, quantity in item.items():
                    if quantity:
                        normalized.append(f"{ing_name}: {quantity}")
                    else:
                        normalized.append(ing_name)
            elif isinstance(item, str):
                if item.strip():
                    normalized.append(item.strip())
            else:
                normalized.append(str(item))
        if normalized:
            return normalized
        else:
            return [
                f"{name} - по вкусу" for name in fallback_ingredient_names
            ]

    if isinstance(ingredients_data, dict):
        normalized = []
        for ing_name, quantity in ingredients_data.items():
            if quantity:
                normalized.append(f"{ing_name}: {quantity}")
            else:
                normalized.append(ing_name)
        return normalized if normalized else [
            f"{name} - по вкусу" for name in fallback_ingredient_names
        ]

    if isinstance(ingredients_data, str):
        parts = re.split(r'[,\n]+', ingredients_data)
        parts = [p.strip() for p in parts if p.strip()]
        if parts:
            return parts
        else:
            return [ingredients_data.strip()]

    return [str(ingredients_data)]
