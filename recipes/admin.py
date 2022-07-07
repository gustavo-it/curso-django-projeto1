from django.contrib import admin

from .models import Category, Recipe


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Registrando elementos na área administrativa
    """


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
