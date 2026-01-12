from django.contrib import admin
from .models import Allergen, Category, Ingredient, Pairing


admin.site.register(Allergen)
admin.site.register(Category)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'allergen', 'nutrition_summary')
    list_filter = ('category', 'allergen')
    search_fields = ('title', 'description')
    list_per_page = 20

    def nutrition_summary(self, obj):
        return obj.nutrition_summary
    nutrition_summary.short_description = "КБЖУ"


@admin.register(Pairing)
class PairingAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient_a',
        'ingredient_b',
        'pairing_type_display'
    )
    list_filter = ('pairing_type',)
    search_fields = ('ingredient_a__title', 'ingredient_b__title')
    autocomplete_fields = ['ingredient_a', 'ingredient_b']

    def pairing_type_display(self, obj):
        return obj.get_pairing_type_display()
    pairing_type_display.short_description = "Тип сочетания"
