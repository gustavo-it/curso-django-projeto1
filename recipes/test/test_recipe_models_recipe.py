from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_defaults(self):
        """
        Criando uma receita específica para os nossos testes a seguir.
        """
        recipe = Recipe(
            category=self.make_category(name="Comida árabe"),
            author=self.make_author(username="Novo usuário"),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        """
        Esste test verifica se ocorre o ValidationError quando
        tentamos cadastrar valores maiores que o permitido.
        """
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_if_false_by_default(self):
        """
        Verifica se de fato o "campo preparations_steps_is_html"
        recebe como valor padrão o False.
        """
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg="Recipe preparation_steps_is_html is not False")

    def test_recipe_is_published_is_false_by_default(self):
        """
        Verifica se de fato o campo "is_published" recebe como valor
        padrão o False.
        """
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(recipe.is_published,
                         msg="Recipe is_published is not False")

    def test_recipe_string_representation(self):
        """
        Verifica se o método __str__ que utilizamos no models
        retorna o título correto da receita.
        """
        self.recipe.title = "Testing Representation"
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), 'Testing Representation')
