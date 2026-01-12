from django.urls import path
from . import views


urlpatterns = [
    path('recommendations/', views.get_pairing_recommendations, name='recommendations'),
    path('search/', views.search_ingredients, name='search'),
    path('generate_recipe/', views.generate_recipe_api, name='generate_recipe'),
]
