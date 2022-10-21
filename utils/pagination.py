import math


def make_pagination_range(page_range, qtd_paginas, current_page):
    """
    Criando uma paginação

    Args:
        page_range (lista): Gera uma lista de N elementos.
        qtd_paginas (int): Quantidade de links que serão exibidos
        ao usuário.
        current_page (int): Página que o usuário está.

    Returns:
        lista: Faz um slicing na quantidade total de páginas e nos retorna
        dois números antes do atual e dois números depois.
    """
    middle_range = math.ceil(qtd_paginas / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    return page_range[start_range:stop_range]
