from django.forms import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category(
            name="Category Testing"
        )
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        """
        Estamos testando se o método mágico __str__ está retornando
        o título correto da nossa category.
        """
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        """
        Testando se ocorre um erro quando tentamos salvar uma categoria
        que extrapole o número de caracteres que definimos em models.
        """
        self.category.name = "A" * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
