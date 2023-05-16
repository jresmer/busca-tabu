from neighbourhood import Neighbourhood
from objFuncCalculator import ObjFuncCalculator
from interfaceManager import InterfaceManager
from csvLogManager import CSVLogManager
import osmnx as ox


class TabuSearch:
    def __init__(self):
        self.__obj_calculator = ObjFuncCalculator()
        self.__nd = Neighbourhood()
        self.__log = None

        self.__best_s = None
        self.__best_s_value = None
        self.__perc = 100

        self.__s = None
        self.__opt_value = None
        self.__interface = InterfaceManager()

        self.__address_list = ['Rua Roberto Sampaio Gonzaga, Florianópolis, Brazil', 'São Paulo, Brazil', 'Balneário Camboriú, Brazil', '350 5th Ave, New York, New York']

    def __set_first_solution(self, address_sel, dist, steps, perc, budget):
        self.__perc = perc

        graph = ox.graph_from_address(self.__address_list[address_sel], network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        self.__s = __graph
        max_bool = True
        # busca construtiva
        while budget > 499:
            max_bool = not max_bool
            best_neighbour, \
                best_neighbours_value, cost = self.__nd.get_best_neighbour_random(self.__s,
                                                                                  budget, max_bool)
            self.__s = best_neighbour
            self.__opt_value = best_neighbours_value
            budget -= cost

        self.__opt_value_5 = self.__opt_value * (self.__perc / 100)

        self.__best_s = self.__s
        self.__best_s_value = self.__opt_value

    def __loop(self, budget):
        max_bool = True
        budget = 0
        while True:
            # reverte uma alteracao recente:
            max_bool = not max_bool
            self.__s, added_budget = self.__nd.reverse_change(self.__s, max_bool)
            budget += added_budget
            # gera um novo vizinho:
            best_neighbour, \
                best_neighbours_value, cost = self.__nd.get_best_neighbour_random(self.__s,
                                                                                  budget, max_bool)
            if best_neighbours_value - self.__opt_value < self.__opt_value_5:
                self.__opt_value = best_neighbours_value
                self.__opt_value_5 = best_neighbours_value * (self.__perc / 100)
                self.__s = best_neighbour
                budget -= cost
                if best_neighbours_value < self.__best_s_value:
                    self.__best_s = best_neighbour
                    self.__best_s_value = best_neighbours_value
            else:
                self.__log.quit(', because no better neighbour was found')
                break

    def get_best_solution(self):
        return self.__best_s

    def get_best_solutions_value(self):
        return self.__best_s_value

    def run(self, address_sel=None, dist=None, steps=None, budget=None, perc=None):
        if address_sel is None:
            address_sel, dist, steps, budget, perc = self.__interface.address_selection(self.__address_list)
        self.__log = CSVLogManager(steps, self.__address_list[address_sel], dist, budget, perc)
        self.__nd.set_log(self.__log)
        self.__set_first_solution(address_sel, dist, steps, perc, budget)
        self.__loop(budget)
        self.__log.quit()
