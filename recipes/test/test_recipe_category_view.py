from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        """
        Verificando se a url category está ligado a view category.
        """
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "This is category test"
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """
        Verificando se é exibido o template 404, através do status code,
        quando não temos receitas na categoria.
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"pk": 12312}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        """
        Verifica se é retornado o erro 404 quando
        não é encontrado uma categoria.
        """
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000}))
        self.assertEqual(response.status_code, 404)
