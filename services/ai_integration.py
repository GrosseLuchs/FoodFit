from .yandex_gpt_client import YandexGPTClient
from .recipe_parser import parse_recipe_from_response

def generate_recipe_ai(ingredient_names, category_names=None):
    """
    Главная функция генерации рецептов.
    """

    print(f"DEBUG: generate_recipe_ai вызвана с ingredient_names={ingredient_names}")

    if not ingredient_names:
        return _get_empty_recipe()
    
    # 1. Пробуем YandexGPT
    client = YandexGPTClient()
    if client.is_configured():
        api_response = client.generate_recipe(ingredient_names)
        if api_response:
            recipe = parse_recipe_from_response(api_response, ingredient_names)
            if recipe:
                print("✅ Рецепт сгенерирован через YandexGPT")
                return recipe
    
    # 2. Возвращаем сообщение об ошибке (вместо примитивной генерации)
    print("❌ YandexGPT недоступен")
    return _get_service_unavailable_recipe(ingredient_names)

def _get_empty_recipe():
    return {
        "title": "Выберите ингредиенты",
        "time": "-",
        "ingredients": [],
        "instructions": "Добавьте ингредиенты для генерации рецепта.",
        "tips": ""
    }

def _get_service_unavailable_recipe(ingredient_names):
    """Возвращает рецепт-заглушку при недоступности сервиса"""
    print(f"DEBUG: Используем fallback рецепт для {ingredient_names}")
    
    # Убедимся, что ingredient_names - это список строк
    if not isinstance(ingredient_names, list):
        ingredient_names = [str(ingredient_names)]
    
    return {
        "title": f"Блюдо из {ingredient_names[0] if ingredient_names else 'ингредиентов'}",
        "time": "30 минут",
        "ingredients": [f"{ing} - по вкусу" for ing in ingredient_names],
        "instructions": "К сожалению, сервис генерации рецептов временно недоступен. Попробуйте позже.",
        "tips": "Вы можете поискать рецепты вручную или попробовать снова через некоторое время."
    }
