from rest_framework import serializers

from backend.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ингредиента.
    Используется в API для получения данных об ингредиентах,
    включая вычисляемые поля nutrition_summary и has_allergen.
    """
    nutrition_summary = serializers.CharField(read_only=True)
    has_allergen = serializers.BooleanField(read_only=True)
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
        )
    allergen = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Ingredient
        fields = [
            'id',
            'title',
            'display_name',
            'category',
            'category_name',
            'allergen',
            'description',
            'calories',
            'protein',
            'fat',
            'carbohydrates',
            'fiber',
            'nutrition_summary',
            'has_allergen',
        ]


class RecipeGenerationSerializer(serializers.Serializer):
    """Сериализатор для запроса генерации рецепта"""
    ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        min_length=1,
        max_length=10
    )
