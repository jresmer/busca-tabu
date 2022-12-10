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
        self.opt_value = self.obj_function_radom(self.s)
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
                value = self.obj_function_radom(s)
                for _s in nd.neighbourhood:
                    _value = self.obj_function_radom(_s)
                    if _value < value:
                        s = _s
                        value = _value
        return s

    # Acelerar com paralelismo:
    def obj_function_radom(self, solution, num_tests=100, attempt_limit=10000) -> float:
        node_list = list(solution.nodes)
        pairs = []
        start = time.time()
        for node1 in node_list:
            for node2 in node_list:
                if nx.has_path(solution, node1, node2):
                    pairs.append((node1, node2))
        end = time.time()
        print(end - start)
        length = len(pairs)

        t_routes = 0
        t_time = 0

        while attempt_limit > 0:
            attempt_limit -= 1

            origin, dest = pairs.pop(randint(0, len(pairs) - 1))

            if origin == dest:
                continue

            shortest_path_length = nx.shortest_path_length(solution, origin, dest,
                                                           weight='travel_time')

            if shortest_path_length != 0:
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
            value = self.obj_function_radom(opt_nb)

            for _s in nd.neighbourhood:
                _value = self.obj_function_radom(_s)
                if _s not in self.tabu_list and _value != 0 and _value < value:
                    value = _value
                    opt_nb = _s

            if self.opt_value >= value:
                self.best_solution = opt_nb

            self.tabu_list.update(self.s)
            self.s = opt_nb

    def get_best_solution(self):
        return self.s
