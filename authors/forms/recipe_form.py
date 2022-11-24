from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


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
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if description == title:
            self._my_errors['description'].append('Cannot be equal to title')
            self._my_errors['title'].append('Cannot be equal to description')

        if self._my_errors:
            raise ValidationError(self._my_errors)

        return super_clean

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if len(title) < 5:
            self._my_errors['title'].append(
                'Title must have at least 5 chars.')
        return title

    def clean_preparation_time(self):
        field_name = 'preparation_time'
        field_value = self.cleaned_data.get(field_name)

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number in preparation time')

        return field_value

    def clean_servings(self):
        field_name = 'servings'
        field_value = self.cleaned_data.get('servings')

        if not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number in servings')

        return field_value
