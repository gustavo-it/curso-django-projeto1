from django.http import Http404
from django.utils.translation import gettext as _

from .base import RecipeListViewBase


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - \
            {category_translation} | '
        })
        return ctx
