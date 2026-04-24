import logging
from django.shortcuts import render
from backend.models import Ingredient

logger = logging.getLogger('foodfit')


def index(request):
    """Главная страница с выбором ингредиентов."""
    ingredients = Ingredient.objects.select_related(
        'category', 'allergen'
    ).order_by('title')
    logger.debug(f"Loaded {ingredients.count()} ingredients for index page")
    return render(request, 'index.html', {'ingredients': ingredients})
