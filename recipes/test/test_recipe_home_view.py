from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
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
