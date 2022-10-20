from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):

    def test_make_pagination_range_returns_a_pagination_range(self):
        """
        Este é um test de paginação.
        pagination --> Gera uma lista de 20 elementos.
        qtd_paginas --> Quantidade de links que queremos exibir
        ao usuário.
        current_page --> página que o usuário está.
        assertEqual --> Compara dois valores. Nesse caso, verifica
        se a lista é igual a pagination.
        """
        pagination = make_pagination_range(page_range=list(range(1, 21)),
                                           qtd_paginas=4,
                                           current_page=1)

        self.assertEqual([1, 2, 3, 4], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(
            self):
        ...
