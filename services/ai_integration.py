import logging

from .yandex_gpt_client import YandexGPTClient
from .recipe_parser import parse_recipe_from_response

logger = logging.getLogger('foodfit')


def generate_recipe_ai(ingredient_names, category_names=None):
    """
    Главная функция генерации рецептов.
    Возвращает словарь с рецептом или словарь с ошибкой (ключ '_error': True).
    """
    if not ingredient_names:
        logger.warning("generate_recipe_ai вызвана без ингредиентов")
        return _get_empty_recipe()

    logger.debug(f"Генерация рецепта для ингредиентов: {ingredient_names}")

    client = YandexGPTClient()
    if client.is_configured():
        api_response = client.generate_recipe(ingredient_names)
        if api_response:
            recipe = parse_recipe_from_response(api_response, ingredient_names)
            if recipe:
                logger.info("Рецепт успешно сгенерирован через YandexGPT")
                return recipe
            else:
                logger.warning("Не удалось распарсить ответ YandexGPT")
        else:
            logger.warning("YandexGPT не вернул ответ (возможно, ошибка API)")
    else:
        logger.warning("YandexGPT не сконфигурирован (отсутствуют ключи)")

    logger.error(
        "Сервис YandexGPT недоступен, возвращаем fallback-рецепт с ошибкой"
    )
    return _get_service_unavailable_recipe(ingredient_names)


def _get_empty_recipe():
    """Пустой рецепт (когда нет ингредиентов)"""
    return {
        "title": "Выберите ингредиенты",
        "time": "-",
        "ingredients": [],
        "instructions": (
            "Добавьте ингредиенты для генерации рецепта."
        ),
        "tips": "",
        "_error": False
    }


def _get_service_unavailable_recipe(ingredient_names):
    """Возвращает рецепт-заглушку при недоступности сервиса с пометкой _error=True"""  # noqa: E501
    if not isinstance(ingredient_names, list):
        ingredient_names = [str(ingredient_names)]

    first = ingredient_names[0] if ingredient_names else 'ингредиентов'
    return {
        "title": f"Блюдо из {first}",
        "time": "—",
        "ingredients": [f"{ing} - по вкусу" for ing in ingredient_names],
        "instructions": (
            "К сожалению, сервис генерации рецептов временно недоступен. "
            "Попробуйте позже."
        ),
        "tips": "",
        "_error": True
    }
