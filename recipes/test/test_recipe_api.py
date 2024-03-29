from unittest.mock import patch

from django.urls import reverse
from rest_framework import test

from recipes.test.test_recipe_base import RecipeMixin


class RecipeAPIv2Test(test.APITestCase, RecipeMixin):
    def get_jwt_access_token(self):
        """
        Método para obter o JWT
        """
        userdata = {
            'username': 'user',
            'password': 'password'
        }
        api_url = reverse('recipes:token_obtain_pair')
        self.make_author(username=userdata.get('username'),
                         password=userdata.get('password'))

        response = self.client.post(
            self.client.get(api_url), data={**userdata})
        return response.get('access')

    def get_recipe_raw_data(self):
        return {
            'title': 'This is the title',
            'description': 'This is the description',
            'preparation_time': 1,
            'preparation_time_unit': 'Minutes',
            'servings': 1,
            'servings_unit': 'Person',
            'preparation_steps': 'This is the preparation steps.'
        }

    def test_recipe_api_list_returns_status_code_200(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        self.assertEqual(response.status_code, 200)

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_number_of_recipes = 10
        self.make_recipe_in_batch(qtd=wanted_number_of_recipes)
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        qtd_of_loaded_recipes = len(response.data.get('results'))
        # print(response.data)
        self.assertEqual(wanted_number_of_recipes, qtd_of_loaded_recipes)

    def test_recipe_api_list_do_not_show_not_published_recipes(self):
        recipes = self.make_recipe_in_batch(qtd=2)
        recipe_not_published = recipes[0]
        recipe_not_published.is_published = False
        recipe_not_published.save()
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.get(api_url)
        # print(response.data)
        self.assertEqual(
            len(response.data.get('results')),
            1
        )

    @patch('recipes.views.api.RecipeAPIv2Pagination.page_size', new=10)
    def test_recipe_api_list_loads_recipes_by_category_id(self):
        category_wanted = self.make_category(name='WANTED_CATEGORY')
        category_not_wanted = self.make_category(name='NOT_WANTED_CATEGORY')
        recipes = self.make_recipe_in_batch(qtd=10)

        for recipe in recipes:
            recipe.category = category_wanted
            recipe.save()
        recipes[0].category = category_not_wanted
        recipes[0].save()

        api_url = reverse('recipes:recipes-api-list') + \
            f'?category_id={category_wanted.id}'
        response = self.client.get(api_url)
        self.assertEqual(
            len(response.data.get('results')),
            9
        )

    def test_recipe_api_list_user_must_send_jwt_token_to_create_recipe(self):
        api_url = reverse('recipes:recipes-api-list')
        response = self.client.post(api_url)
        self.assertEqual(response.status_code, 401)

    def test_jwt_login(self):
        print(self.get_jwt_access_token())

    def test_recipe_api_list_logged_user_can_create_a_recipe(self):
        data = self.get_recipe_raw_data()
        response = self.client.post(
            reverse('recipes:recipes-api-list'),
            data=data,
            HTTP_AUTHORIZATION=f'Bearer {self.get_jwt_access_token()}'
        )

        self.assertEqual(
            response.status_code,
            201
        )
