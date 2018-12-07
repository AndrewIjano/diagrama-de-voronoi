# -*- coding: utf-8 -*-

"""Algoritmos para o Problema do Diagrama de Voronoi:

Dado um conjunto de pontos, determinar o seu diagrama de Voronoi.

Algoritmos disponiveis:
- Algoritmo de Fortune
"""

from . import fortune

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = [
	[ 'fortune', 'Fortune', 'Fortune' ]
]

#children = algorithms

#__all__ = [ 'graham', 'gift' ]
__all__ = [a[0] for a in children]
