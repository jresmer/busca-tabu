from neighbourhood import Neighbourhood
from interfaceManager import InterfaceManager
from csvLogManager import CSVLogManager
import osmnx as ox


class TabuSearch:
    def __init__(self):
        self.__nd = None
        self.__log = None

        self.__best_s = None
        self.__best_s_value = None

        self.__s = None
        self.__opt_value = None
        self.__interface = InterfaceManager()

        self.__address_list = ['Rua Roberto Sampaio Gonzaga, Florianópolis, Brazil', 'São Paulo, Brazil', 'Balneário Camboriú, Brazil', '350 5th Ave, New York, New York']

    def __set_first_solution(self, address_sel, dist, budget):

        graph = ox.graph_from_address(self.__address_list[address_sel], network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        self.__s = __graph
        max_bool = True
        # busca construtiva
        contador = 0
        while budget > 499:
            max_bool = not max_bool
            best_neighbor, \
                best_neighbors_value, cost = self.__nd.parallel_get_best_neighbor(self.__s,
                                                                                  budget, max_bool)
            self.__s = best_neighbor
            self.__opt_value = best_neighbors_value
            budget -= cost
            contador += 1

        self.__best_s = self.__s
        self.__best_s_value = self.__opt_value

    def __loop(self, budget, itr):
        max_bool = True
        budget = 0
        for _ in range(itr):
            # reverte uma alteracao recente:
            max_bool = not max_bool
            self.__s, added_budget = self.__nd.reverse_change(self.__s, max_bool)
            budget += added_budget
            # gera um novo vizinho:
            best_neighbor, \
                best_neighbors_value, cost = self.__nd.parallel_get_best_neighbor(self.__s,
                                                                                  budget, max_bool)
            self.__s = best_neighbor
            budget -= cost
            if best_neighbors_value < self.__best_s_value:
                self.__best_s = best_neighbor
                self.__best_s_value = best_neighbors_value

    def get_best_solution(self):
        return self.__best_s

    def get_best_solutions_value(self):
        return self.__best_s_value

    def run(self, address_sel=None, dist=None, budget=None, tabu_list_size=None, itr=50):
        if address_sel is None:
            address_sel, dist, budget, tabu_list_size, itr = self.__interface.address_selection(self.__address_list)
        self.__nd = Neighbourhood(tabu_list_size)
        self.__log = CSVLogManager(self.__address_list[address_sel], dist, budget, tabu_list_size)
        self.__nd.set_log(self.__log)
        self.__set_first_solution(address_sel, dist, budget)
        self.__loop(budget, itr)
        self.__log.quit()
