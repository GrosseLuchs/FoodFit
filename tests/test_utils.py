import pytest
from backend.utils import get_recommendations_by_type
from backend.models import Pairing

pytestmark = pytest.mark.django_db


class TestGetRecommendations:
    def test_single_ingredient_recommendations(self, chicken, cheese):
        Pairing.objects.create(
            ingredient_a=chicken,
            ingredient_b=cheese,
            pairing_type='cook'
        )
        result = get_recommendations_by_type([chicken.id])
        good_cook_ids = [ing.id for ing in result['good']['cook']]
        assert cheese.id in good_cook_ids
        good_serve_ids = [ing.id for ing in result['good']['serve']]
        assert cheese.id not in good_serve_ids

    def test_pairing_type_filter(self, beef, cheese):
        Pairing.objects.create(
            ingredient_a=beef,
            ingredient_b=cheese,
            pairing_type='serve'
        )
        result = get_recommendations_by_type([beef.id], pairing_type='serve')
        serve_ids = [ing.id for ing in result['good']['serve']]
        assert cheese.id in serve_ids
        assert not result['good']['cook']

    def test_cache_usage(self, chicken, cheese):
        from django.core.cache import cache
        cache.clear()
        Pairing.objects.create(
            ingredient_a=chicken,
            ingredient_b=cheese,
            pairing_type='cook'
        )
        get_recommendations_by_type([chicken.id])
        key = f"recommendations_[{chicken.id}]_None"
        assert cache.get(key) is not None
