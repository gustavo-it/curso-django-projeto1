from django.db.models import Q
from django.http import Http404

from .base import RecipeListViewBase


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(Q(title__icontains=search_term) |
              Q(description__icontains=search_term)
              )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '').strip()
        ctx.update({
            "page_title": f"Search for '{search_term}' |",
            'search_term': search_term,
            'additional_url_query': f"&q={search_term}",
        })
        return ctx
