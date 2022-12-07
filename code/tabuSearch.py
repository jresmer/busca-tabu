from neighbourhood import Neighbourhood
# from pprint import pprint
from tabuList import TabuList
from random import randint
import networkx as nx
import osmnx as ox


class TabuSearch:

    def __init__(self, dist, steps=50):
        self.s = self.get_first_solution(dist, steps)
        self.best_solution = self.s
        self.opt_value = self.obj_function_extremities(self.s)
        self.tabu_list = TabuList()

    # Escolher um vizinho aleatorio
    def get_first_solution(self, dist, steps, random=True):
        graph = ox.graph_from_address('350 5th Ave, New York, New York', network_type='drive', dist=dist)
        _graph = ox.project_graph(graph)
        __graph = ox.utils_graph.get_largest_component(_graph, strongly=True)
        s = __graph
        if random:
            for _ in range(steps):
                nd = Neighbourhood(s)
                s = nd.neighbourhood[randint(0, len(nd.neighbourhood))]
        else:
            for _ in range(steps):
                nd = Neighbourhood(s)
                value = self.obj_function_extremities(s)
                for _s in nd.neighbourhood:
                    _value = self.obj_function_extremities(_s)
                    if _value < value:
                        s = _s
                        value = _value
        return s

    # Acelerar com paralelismo:
    def obj_function_radom(self, solution, num_tests, attempt_limit=10000) -> float:
        node_list = list(solution.nodes)
        already_tested = []
        length = len(node_list)
        randint_length = length - 1

        t_routes = 0
        t_time = 0

        while attempt_limit > 0:
            attempt_limit -= 1

            origin = node_list[randint(0, randint_length)]
            dest = node_list[randint(0, randint_length)]
            already_tested.append((origin, dest))
            print(f' {origin} , {dest}')

            if origin == dest or not nx.has_path(solution, origin, dest) or (origin, dest) in already_tested:
                continue

            print(origin)
            print(dest)

            shortest_path_length = nx.shortest_path_length(solution, origin, dest,
                                                           weight='travel_time')
            if shortest_path_length != 0 and shortest_path_length != None:
                t_time += shortest_path_length
                t_routes += 1

            if t_routes == num_tests:
                break

        if t_routes > 0:
            print(f"Number of paths tested : {t_routes}")
            return t_time / t_routes
        return 0


    def obj_function_extremities(self, solution, num_tests=100) -> float:
        origin = list(solution.nodes)
        origin.sort()
        dest = list(solution.nodes)
        dest.sort(reverse=True)

        t_routes = 0
        t_time = 0

        for i in range(len(origin)):
            if origin == dest or not nx.has_path(solution, origin[i], dest[i]):
                continue

            shortest_path_length = nx.shortest_path_length(solution, origin[i], dest[i],
                                                           weight='travel_time', method='bellman-ford')
            if shortest_path_length != 0 and shortest_path_length != None:
                t_time += shortest_path_length
                t_routes += 1

            if t_routes == num_tests:
                break

        if t_routes > 0:
            print(f"Number of paths tested : {t_routes}")
            return t_time / t_routes
        return 0

    # Terminar get_best_neighbour para substituir generate_neighbourhood:
    def loop(self):
        for _ in range(50):
            nd = Neighbourhood()
            nd.generate_neighbourhood(self.s, self.tabu_list)
            opt_nb = nd.neighbourhood[0]
            value = self.obj_function_extremities(opt_nb)

            for _s in nd.neighbourhood:
                _value = self.obj_function_extremities(_s)
                if _s not in self.tabu_list and _value != 0 and _value < value:
                    value = _value
                    opt_nb = _s

            if self.opt_value >= value:
                self.best_solution = opt_nb

            self.tabu_list.update(self.s)
            self.s = opt_nb

    def get_best_solution(self):
        return self.s
