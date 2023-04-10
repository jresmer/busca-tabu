from neighbourhood import Neighbourhood
from tabuList import TabuList
from objFuncCalculator import ObjFuncCalculator
from interfaceManager import InterfaceManager
from logManager import LogManager
import osmnx as ox


class TabuSearch:
    def __init__(self):
        self.__obj_calculator = ObjFuncCalculator()
        self.__nd = Neighbourhood()

        self.__best_s = None
        self.__best_s_value = None
        self.__perc = 100

        self.__s = None
        self.__opt_value = None
        self.__opt_value_5 = None
        self.__tabu_list = TabuList()
        self.__interface = InterfaceManager()

        self.__address_list = ['Rua Roberto Sampaio Gonzaga, Florianópolis, Brazil', 'São Paulo, Brazil', 'Balneário Camboriú, Brazil', '350 5th Ave, New York, New York']

    def __set_first_solution(self, address_sel, dist, steps, perc):
        self.__perc = perc

        graph = ox.graph_from_address(self.__address_list[address_sel], network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        s = __graph
        for _ in range(steps):
            s = self.__nd.random_neighbour(s)

        self.__s = s
        self.__opt_value = self.__obj_calculator.obj_func_random(s)
        self.__opt_value_5 = self.__opt_value * (self.__perc / 100)

        self.__best_s = s
        self.__best_s_value = self.__opt_value

    def __loop(self, budget):
        max_bool = True
        while budget > 0:
            max_bool = not max_bool
            best_neighbour, \
                best_neighbours_value, cost = self.__nd.get_best_neighbour_random(self.__s,
                                                                                  budget, max_bool,
                                                                                  tabu_list=self.__tabu_list)
            if best_neighbours_value not in self.__tabu_list and \
                    best_neighbours_value - self.__opt_value < self.__opt_value_5:
                self.__tabu_list.update(best_neighbour)
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

    def run(self):
        address_sel, dist, steps, budget, perc = self.__interface.address_selection(self.__address_list)
        self.__log = LogManager(steps)
        self.__set_first_solution(address_sel, dist, steps, perc)
        self.__loop(budget)
        self.__log.quit()

        ox.plot_graph(self.get_best_solution())
