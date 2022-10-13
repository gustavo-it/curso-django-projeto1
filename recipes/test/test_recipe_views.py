from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        """
        Checar se a url home está ligado a view home.
        """
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        """
        Verificar o status code da url.
        """
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        """
        Checar se a url home está renderizando o template correto.
        """
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        """
        Verificando se o template é exibido corretamente, quando não temos
        receitas cadastradas.
        """
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Ainda não temos receitas cadastradas",
                      response.content.decode('utf-8'))

    def test_recipe_home_template_loads_recipes(self):
        """
        Estamos verificando se o título da receita e descrição
        estão sendo renderizados em nosso template home.
        """
        self.make_recipe()
        response = self.client.get(reverse("recipes:home"))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('Recipe Description', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """
        Agora com receitas, verificamos se o conteúdo de assertIn
        é exibido quando não temos receitas publicadas.
        """
        self.make_recipe(is_published=False)
        response = self.client.get(reverse("recipes:home"))

        self.assertIn("Ainda não temos receitas cadastradas",
                      response.content.decode('utf-8'))

    def test_recipe_category_view_function_is_correct(self):
        """
        Verificando se a url category está ligado a view category.
        """
        view = resolve(reverse("recipes:category", kwargs={"category_id": 1}))
        self.assertIs(view.func, views.category)

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
            reverse("recipes:recipe", kwargs={"id": recipe.category.id}))

        self.assertEqual(response.status_code, 404)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        """
        Verifica se é retornado o erro 404 quando não é encontrado uma categoria.
        """
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        """
        Checando se a url de detalhes da receita, está ligada a view da receita.
        """
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        """
        Verifica se é retornado o erro 404 quando não é encontrado a url
        da receita.
        """
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipes(self):
        """
        Verificando se a receita está sendo exibida corretamente no template.
        """
        needed_title = "This is a detail page - it load one recipe"
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1}))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """
        Verifica se é retornado o erro 404 quando a url da receita
        não é encontrado, ou seja, quando a receita não existe.
        """
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": recipe.id}))

        self.assertEqual(response.status_code, 404)
