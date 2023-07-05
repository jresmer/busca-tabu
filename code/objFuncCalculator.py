from random import choice
import networkx as nx


class ObjFuncCalculator:

    @staticmethod
    def random_obj_func(solution, num_tests=300, attempt_limit=10000) -> float:
        nodes = list(solution.nodes)
        pair_list = []

        t_routes = 0
        t_time = 0

        while attempt_limit > 0:

            origin = choice(nodes)
            dest = choice(nodes)

            if (origin, dest) in pair_list or not nx.has_path(solution, origin, dest):
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
