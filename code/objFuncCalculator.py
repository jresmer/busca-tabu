from random import choice
import networkx as nx


class ObjFuncCalculator:

    def __init__(self) -> None:
        self.__tested_pairs = []

    def random_obj_func(self, solution, num_tests=100, attempt_limit=10000) -> float:
        edges = [e for e in solution.edges]
        pair_list = []

        t_routes = 0
        t_time = 0

        while attempt_limit > 0:
            length = len(edges) - 1
            if length == -1:
                break

            origin, dest, k = choice(edges)

            if (origin, dest) in pair_list:
                continue

            pair_list.append((origin, dest))

            shortest_path_length = nx.shortest_path_length(solution, origin, dest,
                                                           weight='travel_time')
            
            t_time += shortest_path_length
            t_routes += 1

            if t_routes == num_tests:
                break

        if t_routes > 0:
            return t_time / t_routes
        return 0
