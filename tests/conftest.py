import pytest
from rest_framework.test import APIClient
from backend.models import Category, Allergen, Ingredient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category():
    return Category.objects.create(name="Мясо")


@pytest.fixture
def allergen():
    return Allergen.objects.create(name="Лактоза", code="L")


@pytest.fixture
def chicken(category):
    return Ingredient.objects.create(
        title="Курица",
        display_name="Курица",
        category=category,
        calories=165,
        protein=31,
        fat=3.6
    )


@pytest.fixture
def cheese(category):
    return Ingredient.objects.create(
        title="Сыр",
        display_name="Сыр",
        category=category,
        calories=402,
        protein=25,
        fat=33
    )


@pytest.fixture
def beef(category):
    return Ingredient.objects.create(
        title="Говядина",
        display_name="Говядина",
        category=category,
        calories=250,
        protein=26,
        fat=15
    )
