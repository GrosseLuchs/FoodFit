import logging
from collections import defaultdict

from django.db.models import Q
from django.core.cache import cache

from backend.models import Pairing, Ingredient

logger = logging.getLogger('foodfit')


def get_recommendations_by_type(selected_ingredient_ids, pairing_type=None):
    """
    Возвращает рекомендации с учетом типа сочетания.
    """
    cache_key = (
        f"recommendations_{sorted(selected_ingredient_ids)}_{pairing_type}"
    )
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        logger.debug(
            "Рекомендации получены из кэша (ключ: %s)", cache_key
        )
        return cached_result

    if not selected_ingredient_ids:
        result = {'good': {'cook': [], 'serve': []}, 'bad': []}
        cache.set(cache_key, result, 300)
        return result

    selected_ids_set = set(selected_ingredient_ids)

    pairing_filters = (
        Q(ingredient_a__in=selected_ids_set)
        | Q(ingredient_b__in=selected_ids_set)
    )
    if pairing_type:
        pairing_filters &= Q(pairing_type=pairing_type)

    pairings = Pairing.objects.filter(pairing_filters).select_related(
        'ingredient_a', 'ingredient_b'
    )

    good_partners_by_type = {
        'cook': defaultdict(set),
        'serve': defaultdict(set)
    }

    for pairing in pairings:
        if pairing.ingredient_a.id in selected_ids_set:
            selected_id = pairing.ingredient_a.id
            partner_id = pairing.ingredient_b.id
        else:
            selected_id = pairing.ingredient_b.id
            partner_id = pairing.ingredient_a.id

        good_partners_by_type[
            pairing.pairing_type
        ][selected_id].add(partner_id)

    good_ingredients_by_type = {'cook': set(), 'serve': set()}

    for pt in ['cook', 'serve']:
        if not good_partners_by_type[pt]:
            continue

        first_selected = next(iter(selected_ids_set))
        common = good_partners_by_type[pt].get(first_selected, set())

        for selected_id in selected_ids_set:
            if selected_id == first_selected:
                continue
            partners = good_partners_by_type[pt].get(selected_id, set())
            common &= partners
            if not common:
                break

        good_ingredients_by_type[pt] = common

    all_ingredient_ids = set(
        Ingredient.objects.values_list('id', flat=True)
    )
    all_good_ids = (
        good_ingredients_by_type['cook'] | good_ingredients_by_type['serve']
    )
    bad_ids = all_ingredient_ids - selected_ids_set - all_good_ids

    good_cook = Ingredient.objects.filter(
        id__in=good_ingredients_by_type['cook']
    )
    good_serve = Ingredient.objects.filter(
        id__in=good_ingredients_by_type['serve']
    )
    bad = Ingredient.objects.filter(id__in=bad_ids)

    result = {
        'good': {'cook': good_cook, 'serve': good_serve},
        'bad': bad
    }

    cache.set(cache_key, result, 300)
    logger.debug(
        "Рекомендации вычислены и сохранены в кэш (ключ: %s)", cache_key
    )
    return result
