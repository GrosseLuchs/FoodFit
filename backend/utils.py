from collections import defaultdict
from django.db.models import Q
from django.core.cache import cache
from backend.models import Pairing, Ingredient


def get_recommendations_by_type(selected_ingredient_ids, pairing_type=None):
    """
    Возвращает рекомендации с учетом типа сочетания.
    """

    cache_key = f"recommendations_{sorted(selected_ingredient_ids)}_{pairing_type}"

    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    if not selected_ingredient_ids:
        result = {'good': {'cook': [], 'serve': []}, 'bad': []}
        cache.set(cache_key, result, 300)
        return result

    # Преобразуем в set для быстрых операций
    selected_ids_set = set(selected_ingredient_ids)

    # Шаг 1: Находим ВСЕ сочетания, где участвуют выбранные ингредиенты
    pairing_filters = Q(ingredient_a__in=selected_ids_set) | Q(ingredient_b__in=selected_ids_set)
    if pairing_type:
        pairing_filters &= Q(pairing_type=pairing_type)

    # Используем select_related для загрузки связанных объектов
    pairings = Pairing.objects.filter(pairing_filters)\
        .select_related('ingredient_a', 'ingredient_b')

    # Шаг 2: Собираем сочетающихся "партнеров" по типам
    good_partners_by_type = {
        'cook': defaultdict(set),  # {selected_id: {partner_id1, partner_id2}}
        'serve': defaultdict(set)
    }

    for pairing in pairings:
        # Определяем кто selected, кто partner
        if pairing.ingredient_a.id in selected_ids_set:
            selected_id = pairing.ingredient_a.id
            partner_id = pairing.ingredient_b.id
        else:
            selected_id = pairing.ingredient_b.id
            partner_id = pairing.ingredient_a.id

        # Добавляем в соответствующий тип
        good_partners_by_type[pairing.pairing_type][selected_id].add(partner_id)

    # Шаг 3: Находим пересечение - партнеров, которые сочетаются со ВСЕМИ выбранными
    good_ingredients_by_type = {'cook': set(), 'serve': set()}

    for pairing_type_key in ['cook', 'serve']:
        if not good_partners_by_type[pairing_type_key]:
            continue

        # Начинаем с партнеров первого выбранного ингредиента
        first_selected = next(iter(selected_ids_set))
        common_partners = good_partners_by_type[pairing_type_key].get(first_selected, set())

        # Находим пересечение со всеми остальными выбранными
        for selected_id in selected_ids_set:
            if selected_id == first_selected:
                continue

            selected_partners = good_partners_by_type[pairing_type_key].get(selected_id, set())
            common_partners &= selected_partners  # операция пересечения множеств

            # Если пересечение стало пустым, дальше можно не проверять
            if not common_partners:
                break

        good_ingredients_by_type[pairing_type_key] = common_partners

    # Шаг 4: Все остальные ингредиенты - "плохие"
    all_ingredient_ids = set(Ingredient.objects.values_list('id', flat=True))
    all_good_ids = good_ingredients_by_type['cook'] | good_ingredients_by_type['serve']
    bad_ids = all_ingredient_ids - selected_ids_set - all_good_ids

    # Шаг 5: Загружаем объекты ингредиентов
    good_cook = Ingredient.objects.filter(id__in=good_ingredients_by_type['cook'])
    good_serve = Ingredient.objects.filter(id__in=good_ingredients_by_type['serve'])
    bad = Ingredient.objects.filter(id__in=bad_ids)

    result = {
        'good': {
            'cook': good_cook,
            'serve': good_serve
        },
        'bad': bad
    }

    cache.set(cache_key, result, 300)

    return result
