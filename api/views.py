from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from backend.utils import get_recommendations_by_type
from backend.models import Ingredient
from api.serializers import IngredientSerializer, RecipeGenerationSerializer


@api_view(['GET'])
def get_pairing_recommendations(request):
    """
    API endpoint для получения рекомендаций по сочетаниям.
    """
    ingredient_ids = request.GET.get('ingredient_ids', '')
    pairing_type = request.GET.get('pairing_type', None)

    if not ingredient_ids:
        return Response(
            {'error': 'Не указаны ingredient_ids'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        ingredient_ids_list = [int(id.strip()) for id in ingredient_ids.split(',')]
    except ValueError:
        return Response(
            {'error': 'Неверный формат ingredient_ids'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Используем оптимизированную функцию
    recommendations = get_recommendations_by_type(ingredient_ids_list, pairing_type)

    # Сериализуем данные
    serializer = IngredientSerializer

    result = {
        'selected_ingredients': serializer(
            Ingredient.objects.filter(id__in=ingredient_ids_list),
            many=True
        ).data,
        'good_for_cooking': serializer(recommendations['good']['cook'], many=True).data,
        'good_for_serving': serializer(recommendations['good']['serve'], many=True).data,
        'bad': serializer(recommendations['bad'], many=True).data
    }

    return Response(result)


@api_view(['GET'])
def search_ingredients(request):
    """Поиск ингредиентов по названию"""
    query = request.GET.get('search', '').strip()
    if len(query) < 2:
        return Response([])

    ingredients = Ingredient.objects.filter(
        Q(title__icontains=query) | Q(display_name__icontains=query)
    ).select_related('category', 'allergen')[:10]

    serializer = IngredientSerializer(ingredients, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def generate_recipe_api(request):
    """Генерация рецепта из выбранных ингредиентов с помощью AI"""
    serializer = RecipeGenerationSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(
            {'error': 'Неверные данные', 'details': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    ingredient_ids = serializer.validated_data['ingredient_ids']

    # Получаем ингредиенты с категориями
    ingredients = Ingredient.objects.filter(id__in=ingredient_ids).select_related('category')
    ingredient_names = [ing.title for ing in ingredients]
    category_names = [ing.category.name if ing.category else 'Другое' for ing in ingredients]

    # Генерируем рецепт через AI
    try:
        from services.ai_integration import generate_recipe_ai
        recipe = generate_recipe_ai(ingredient_names, category_names)
    except Exception as e:
        print(f"Ошибка при генерации рецепта: {e}")
        recipe = {
            "title": f"Блюдо из {len(ingredient_names)} ингредиентов",
            "time": "30 минут",
            "ingredients": ingredient_names,
            "instructions": "1. Подготовьте все ингредиенты.\n2. Приготовьте по своему вкусу.\n3. Подавайте и наслаждайтесь!",
            "tips": "Экспериментируйте со специями и пропорциями!"
        }

    return Response(recipe)
