# -*- coding: utf-8 -*-
from networkx import graph_edit_distance


class TabuList:

    # CRIA LISTA DE SOLUCOES
    # SETTA NUMERO DE ITERACOES QUE UMA SOLUCAO DEVE PERMANECER NA LISTA
    def __init__(self, iteration_counter=2, *args):
        self.__iteration_counter = iteration_counter
        self.__iteration_reset_value = iteration_counter
        self.__list = list(args)

    # MAGIC METHOD CHECAGEM IN
    def __contains__(self, item):
        for _solution in self.__list:
            if graph_edit_distance(item, _solution) == 0:
                return True
        return False

    # ADICIONA E REMOVE SOLUCOES TABU
    def update(self, item=None):
        if item is not None:
            self.__list.append(item)
        self.__iteration_counter -= 1
        if self.__iteration_counter < 1:
            self.__list.pop(0)
            self.__iteration_counter = self.__iteration_reset_value
