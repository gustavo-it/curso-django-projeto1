from collections import defaultdict

from django import forms

from authors.validators import AuthorsRecipeValidator
from recipes.models import Recipe
from utils.django_forms import add_attr


class AuthorsRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')
        add_attr(self.fields.get('cover'), 'class', 'span-2')
        add_attr(self.fields.get('category'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = ('title', 'description', 'preparation_time',
                  'preparation_time_unit', 'servings', 'servings_unit',
                  'preparation_steps', 'category', 'cover')

        widgets = {
            'cover':
            forms.FileInput(attrs={'class': 'span-2'}),
            'servings_unit':
            forms.Select(choices=(
                ('Porções', 'Porções'),
                ('Pedaços', 'Pedaços'),
                ('Pessoas', 'Pessoas'),
            ), ),
            'preparation_time_unit':
            forms.Select(choices=(
                ('Horas', 'Horas'),
                ('Minutos', 'Minutos'),
                ('Dias', 'Dias'),
            ))
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        AuthorsRecipeValidator(self.cleaned_data)
        return super_clean
