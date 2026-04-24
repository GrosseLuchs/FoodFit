import pytest
from rest_framework import status
from backend.models import Pairing

pytestmark = pytest.mark.django_db


class TestSearchAPI:
    def test_empty_query(self, api_client):
        response = api_client.get('/api/search/?search=')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_short_query(self, api_client):
        response = api_client.get('/api/search/?search=а')
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_search_found(self, api_client, chicken):
        url = '/api/search/?search=Курица'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert data[0]['title'] == "Курица"


class TestRecommendationsAPI:
    def test_missing_ingredient_ids(self, api_client):
        response = api_client.get('/api/recommendations/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'error' in response.json()

    def test_invalid_ingredient_ids(self, api_client):
        url = '/api/recommendations/?ingredient_ids=abc,def'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_valid_request(self, api_client, chicken, cheese):
        Pairing.objects.create(
            ingredient_a=chicken,
            ingredient_b=cheese,
            pairing_type='cook'
        )
        url = f'/api/recommendations/?ingredient_ids={chicken.id}'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'good_for_cooking' in data
        good_ids = [item['id'] for item in data['good_for_cooking']]
        assert cheese.id in good_ids


class TestGenerateRecipeAPI:
    def test_empty_ingredients(self, api_client):
        response = api_client.post(
            '/api/generate_recipe/',
            {'ingredient_ids': []},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_ingredient_ids(self, api_client):
        response = api_client.post(
            '/api/generate_recipe/',
            {},
            format='json'
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
