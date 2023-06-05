# -*- coding: utf-8 -*-


class TabuList:

    # CRIA LISTA DE SOLUCOES
    # SETTA NUMERO DE ITERACOES QUE UMA SOLUCAO DEVE PERMANECER NA LISTA
    def __init__(self, max_size: int, *args):
        self.__max_size = max_size
        self.__list = list(args)

    # MAGIC METHOD CHECAGEM IN
    def __contains__(self, item):
        return item in self.__list

    # ADICIONA E REMOVE SOLUCOES TABU
    def update(self, item=None):
        if item is not None and item not in self.__list:
            self.__list.append(item)
        if len(self.__list) > self.__max_size:
            self.__list.pop(0)

    def size_getter(self):
        return len(self.__list)

    def erase(self):
        self.__list = []
        self.__size = 0

    def index(self, data):
        return self.__list.index(data)

    def pop(self, index=-1):
        return self.__list.pop(index)
