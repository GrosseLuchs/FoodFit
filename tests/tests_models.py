import pytest
from backend.models import Ingredient, Pairing
from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestIngredientModel:
    def test_nutrition_summary(self, category):
        ing = Ingredient.objects.create(
            title="Яблоко",
            category=category,
            calories=52,
            protein=0.3,
            fat=0.2,
            carbohydrates=14.0
        )
        assert "52 ккал" in ing.nutrition_summary
        assert "Б: 0.3г" in ing.nutrition_summary

    def test_has_allergen_false(self):
        ing = Ingredient.objects.create(title="Морковь")
        assert ing.has_allergen is False

    def test_has_allergen_true(self, allergen):
        ing = Ingredient.objects.create(
            title="Молоко", allergen=allergen
        )
        assert ing.has_allergen is True

    def test_display_name_auto_fill(self):
        long_title = (
            "Очень длинное название ингредиента, "
            "которое не помещается в 50 символов"
        )
        ing = Ingredient.objects.create(title=long_title)
        assert len(ing.display_name) <= 50
        assert ing.display_name.endswith('...')


class TestPairingModel:
    def test_cannot_pair_same_ingredient(self, chicken):
        with pytest.raises(ValidationError):
            pairing = Pairing(
                ingredient_a=chicken,
                ingredient_b=chicken,
                pairing_type='cook'
            )
            pairing.full_clean()

    def test_ordering_swap(self, chicken, cheese):
        Pairing.objects.create(
            ingredient_a=chicken,
            ingredient_b=cheese,
            pairing_type='cook'
        )
        exists = Pairing.objects.filter(
            ingredient_a=chicken,
            ingredient_b=cheese
        ).exists()
        assert exists is True
