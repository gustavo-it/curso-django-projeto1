from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        """
        Testa se o título tem mais de 65 caracteres.
        """
        self.recipe.title = 'A' * 70

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # Aqui acontece a validação
