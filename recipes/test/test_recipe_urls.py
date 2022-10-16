from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_correct(self):
        """
        Teste para a url principal(home).
        """
        url = reverse("recipes:home")
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        """
        Teste para a url de categoria.
        """
        url = reverse("recipes:category", kwargs={"category_id": 1})
        self.assertEqual(url, "/recipes/category/1/")

    def test_recipe_detail_url_is_correct(self):
        """
        Teste a url de detalhes da receita.
        """
        url = reverse("recipes:recipe", kwargs={"id": 1})
        self.assertEqual(url, "/recipes/1/")

    def test_recipe_search_url_is_correct(self):
        """
        Testando a url search da página principal.
        """
        url = reverse("recipes:search")
        self.assertEqual(url, "/recipes/search/")
