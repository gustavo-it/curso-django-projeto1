from django.db.models import Q

from .base_view import RecipeListViewBase


class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
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
