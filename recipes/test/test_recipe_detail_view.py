from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        """
        Checando se a url de detalhes da receita, está ligada
        a view da receita.
        """
        view = resolve(reverse("recipes:recipe", kwargs={"pk": 1}))
        self.assertIs(view.func.view_class, views.RecipeDetail)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """
        Verifica se é retornado o erro 404 quando não é encontrado a url
        da receita.
        """
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        """
        Verificando se a receita está sendo exibida corretamente no template.
        """
        needed_title = "This is a detail page - it load one recipe"
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": 1}))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """
        Verifica se é retornado o erro 404 quando a url da receita
        não é encontrado, ou seja, quando a receita não existe.
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": 2}))

        self.assertEqual(response.status_code, 404)
