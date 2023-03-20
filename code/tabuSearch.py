from neighbourhood import Neighbourhood
from tabuList import TabuList
from objFuncCalculator import ObjFuncCalculator
from interfaceManager import InterfaceManager
import osmnx as ox


class TabuSearch:
    def __init__(self):
        self.__obj_calculator = ObjFuncCalculator()
        self.__nd = Neighbourhood()
        self.__s = None
        self.__opt_value = None
        self.__tabu_list = TabuList()
        self.__interface = InterfaceManager()

        self.__address_list = []

    def set_first_solution(self, address_sel, dist, steps):
        graph = ox.graph_from_address(self.__address_list[address_sel], network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        s = __graph
        for _ in range(steps):
            s = Neighbourhood().random_neighbour(s)

        self.__s = s
        self.__opt_value = self.__obj_calculator.obj_func_random(s)

    def loop(self, budget, max_bool, steps):
        while budget > 0:
            best_neighbour, \
                best_neighbours_value, cost = self.__nd.get_best_neighbour_random(self.__s,
                                                                                  budget, max_bool, steps,
                                                                                  tabu_list=self.__tabu_list)
            if best_neighbours_value < self.__opt_value:
                self.__opt_value = best_neighbours_value
                self.__s = best_neighbour
                budget -= cost
            else:
                # log message
                break

    def get_best_solution(self):
        return self.__s

    def run(self):
        address_sel, dist, steps, budget, max_bool = self.__interface.address_selection(self.__address_list)
        self.set_first_solution(address_sel, dist, steps)
        self.loop(budget, max_bool, steps)

        return self.get_best_solution()
