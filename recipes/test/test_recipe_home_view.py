from unittest.mock import patch

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

    @patch("recipes.views.PER_PAGE", new=3)
    def test_recipe_home_is_paginated(self):
        """
        Criando um teste de paginção para a view home
        Esta recebendo um patch, onde altera o valor de uma variável externa
        para um novo valor e depois volta com o valor antigo, isso para não
        quebrar nosso test.
        Em seguida fazemos um laço para gerar 9 receitas, onde o author_data
        espera um dicionário e o slug é único para cada receita.
        Pegamos o paginator através de context["recipes"], pois estamos
        envolvendo a nossa queryset com o paginator.
        na variável paginator pegamos o paginator para ter acesso a alguns
        elementos.
        Por último:
        Verificamos se o número de paáginas em paginação é 3
        Verificando se na 1°, 2° e 3° página são exibidas de fato 3 receitas.
        """
        for i in range(9):
            kwargs = {"slug": f"r{i}", "author_data": {"username": f"u{i}"}}
            self.make_recipe(**kwargs)

        response = self.client.get(reverse("recipes:home"))
        recipes = response.context["recipes"]
        paginator = recipes.paginator

        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(len(paginator.get_page(2)), 3)
        self.assertEqual(len(paginator.get_page(3)), 3)
