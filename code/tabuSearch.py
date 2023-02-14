from neighbourhood import Neighbourhood
# from pprint import pprint
from tabuList import TabuList
from random import randint
from objFuncCalculator import ObjFuncCalculator
import osmnx as ox

class TabuSearch:
    def __init__(self, dist, steps=50):
        self.__obj_calculator = ObjFuncCalculator()
        self.__nd = Neighbourhood()
        self.s = self.get_first_solution(dist, steps)
        self.best_solution = self.s
        self.opt_value = self.__obj_calculator.obj_func_random(self.s)
        self.tabu_list = TabuList()

    # Escolher um vizinho aleatorio
    def get_first_solution(self, dist, steps, random=True):
        graph = ox.graph_from_address('350 5th Ave, New York, New York', network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        s = __graph
        if random:
            for _ in range(steps):
                nd = Neighbourhood()
                nd.generate_neighbourhood(s)
                s = nd.neighbourhood[randint(0, len(nd.neighbourhood))]
        else:
            for _ in range(steps):
                nd = Neighbourhood()
                nd.generate_neighbourhood(s)
                value = self.__obj_calculator.obj_func_random(s)
                for _s in nd.neighbourhood:
                    _value = self.__obj_calculator.obj_func_random(_s)
                    if _value < value:
                        s = _s
                        value = _value
        return s

    # Terminar get_best_neighbour para substituir generate_neighbourhood:
    def loop(self, itr=50):
        for _ in range(itr):
            best_neighbour, best_neighbours_value = self.__nd.get_best_neighbour(self.s, self.tabu_list)
            if best_neighbours_value < self.opt_value:
                self.opt_value = best_neighbours_value
                self.s = best_neighbour
            else:
                print("No neighbour satisfied the criteria")
                break

    def get_best_solution(self):
        return self.s
