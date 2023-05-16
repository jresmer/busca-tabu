# -*- coding: utf-8 -*-


class TabuList:

    # CRIA LISTA DE SOLUCOES
    # SETTA NUMERO DE ITERACOES QUE UMA SOLUCAO DEVE PERMANECER NA LISTA
    def __init__(self, iteration_counter=10, *args):
        self.__iteration_counter = iteration_counter
        self.__iteration_reset_value = iteration_counter
        self.__list = list(args)

    # MAGIC METHOD CHECAGEM IN
    def __contains__(self, item):
        return item in self.__list

    # ADICIONA E REMOVE SOLUCOES TABU
    def update(self, item=None):
        if item is not None and item not in self.__list:
            self.__list.append(item)
        self.__iteration_counter -= 1
        if self.__iteration_counter < 1:
            self.__list.pop(0)
            self.__iteration_counter = self.__iteration_reset_value

    def index(self, data):
        return self.__list.index(data)

    def pop(self, index=-1):
        return self.__list.pop(index)
