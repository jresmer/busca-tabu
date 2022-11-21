import networkx as nx
from tabuList import TabuList


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

            return cls._instances[cls]


class Neighbourhood(metaclass=SingletonMeta):

    def __init__(self, solution, tabu_list=TabuList()):
        self.__neighbourhood = []
        self.generate_neighbourhood(solution, tabu_list)

    @property
    def neighbourhood(self):
        return self.__neighbourhood

    def generate_neighbourhood(self, solution, tabu_list):
        pass
