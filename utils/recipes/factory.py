# from inspect import signature
from random import randint

from faker import Faker


def rand_ratio():
    return randint(840, 900), randint(473, 573)


fake = Faker('pt_BR')
# print(signature(fake.random_number))


def make_recipe():
    return {
        'id': fake.random_number(digits=2, fix_len=True),
        'title': fake.sentence(nb_words=6),  # Titulo da pagina
        'description': fake.sentence(nb_words=12),  # Descrição
        'preparation_time': fake.random_number(digits=2, fix_len=True),
        # Tempo de preparo da receita
        'preparation_time_unit': 'Minutos',
        # Unidade do tempo de preparo. Horas ou minutos.
        'servings': fake.random_number(digits=2, fix_len=True),
        # Porções
        'servings_unit': 'Porção',
        # Unidade, se é porção ou pessoa, por exemplo.
        'preparation_steps': fake.text(3000),
        # O tempo de preparação.
        'created_at': fake.date_time(),
        # Data que foi criada.
        'author': {
            'first_name': fake.first_name(),
            # Primeiro nome do autor.
            'last_name': fake.last_name(),
            # último nome do autor.
        },
        'category': {
            'name': fake.word()  # Categoria
        },
        'cover': {
            'url': 'https://loremflickr.com/%s/%s/food,cook' % rand_ratio(),
            # Imagem da receita. Utilizando site que gera imagens aleatórias.
        }
    }


if __name__ == '__main__':
    from pprint import pprint
    pprint(make_recipe())
