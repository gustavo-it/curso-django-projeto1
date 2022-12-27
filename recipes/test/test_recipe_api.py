from rest_framework import test

from recipes.test.test_recipe_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    ...
