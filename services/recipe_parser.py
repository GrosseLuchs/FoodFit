import json
import re


def parse_recipe_from_response(api_response, ingredient_names):
    """Парсит рецепт из ответа API"""
    if not api_response or 'result' not in api_response:
        return None

    try:
        text = api_response['result']['alternatives'][0]['message']['text']
        text = _clean_response_text(text)

        # Пытаемся распарсить JSON
        try:
            recipe = json.loads(text)
        except json.JSONDecodeError:
            recipe = _extract_json_from_text(text)

        return _validate_recipe(recipe, ingredient_names)
    except Exception as e:
        print(f"Parse error: {e}")
        return None

def _clean_response_text(text):
    """Очищает текст ответа"""
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    if text.endswith('```'):
        text = text[:-3]
    return text.strip()

def _extract_json_from_text(text):
    """Извлекает JSON из текста"""
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except:
        pass

    # Fallback: создаем структуру из текста
    return _parse_text_to_recipe(text)

def _parse_text_to_recipe(text):
    """Парсит текстовый рецепт в структуру"""
    # Упрощенная реализация (можно расширить)
    lines = text.strip().split('\n')

    recipe = {
        "title": "Рецепт от YandexGPT",
        "time": "30 минут",
        "ingredients": [],
        "instructions": "",
        "tips": ""
    }

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if 'название:' in line.lower():
            recipe['title'] = line.split(':', 1)[1].strip()
        elif 'время:' in line.lower():
            recipe['time'] = line.split(':', 1)[1].strip()

    return recipe

def _validate_recipe(recipe, ingredient_names):
    """Валидирует и дополняет рецепт"""
    required_fields = ['title', 'time', 'ingredients', 'instructions', 'tips']

    for field in required_fields:
        if field not in recipe:
            recipe[field] = ""

    if not recipe['title']:
        recipe['title'] = f"Блюдо из {ingredient_names[0]}"

    # ОБРАБОТКА ИНГРЕДИЕНТОВ - ФИКСИМ ФОРМАТ
    if not recipe.get('ingredients'):
        recipe['ingredients'] = [f"{ing} - по вкусу" for ing in ingredient_names]
    else:
        # Если ingredients - это словарь (объект), преобразуем в массив строк
        if isinstance(recipe['ingredients'], dict):
            ingredients_list = []
            for item, quantity in recipe['ingredients'].items():
                if quantity and quantity.strip():
                    ingredients_list.append(f"{item}: {quantity}")
                else:
                    ingredients_list.append(f"{item}")
            recipe['ingredients'] = ingredients_list
        # Если это список словарей
        elif isinstance(recipe['ingredients'], list) and recipe['ingredients'] and isinstance(recipe['ingredients'][0], dict):
            ingredients_list = []
            for item_dict in recipe['ingredients']:
                for item, quantity in item_dict.items():
                    if quantity and quantity.strip():
                        ingredients_list.append(f"{item}: {quantity}")
                    else:
                        ingredients_list.append(f"{item}")
            recipe['ingredients'] = ingredients_list
        # Если это просто список, убедимся что все элементы - строки
        elif isinstance(recipe['ingredients'], list):
            recipe['ingredients'] = [str(item).strip() for item in recipe['ingredients']]
        # Если это что-то другое
        else:
            recipe['ingredients'] = [str(recipe['ingredients'])]

    if not recipe['instructions']:
        recipe['instructions'] = "1. Подготовьте ингредиенты.\n2. Приготовьте по своему вкусу."

    if not recipe['tips']:
        recipe['tips'] = "Подавайте горячим для лучшего вкуса."

    return recipe
