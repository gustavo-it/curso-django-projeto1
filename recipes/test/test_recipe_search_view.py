from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        """
        Testando se a url search, vai usar a view correta.
        """
        view = resolve(reverse("recipes:search"))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        """
        Verificando o template se a view está carregando
        o template correto.
        """
        response = self.client.get(reverse("recipes:search") + "?q=teste")
        self.assertTemplateUsed(response, "recipes/pages/search.html")

    def test_recipe_search_raises_404_if_no_search_term(self):
        """
        Testando o erro 404 quando não temos um termo no campo
        de busca.
        """
        response = self.client.get(reverse("recipes:search"))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        """
        Testa se o search_term está no título da página e está escapado.
        """
        url = reverse("recipes:search") + "?q=Teste"
        response = self.client.get(url)
        self.assertIn(
            "Search for &#x27;Teste&#x27;",
            response.content.decode("utf-8")
        )
