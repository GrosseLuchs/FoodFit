from django.shortcuts import render
from backend.models import Ingredient


def index(request):
    """Главная страница с выбором ингредиентов"""
    ingredients = Ingredient.objects.all().order_by('title')
    return render(request, 'index.html', {
        'ingredients': ingredients
    })
