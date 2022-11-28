import os

from .base import RecipeListViewBase

PER_PAGE = int(os.environ.get("PER_PAGE", 6))


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'
