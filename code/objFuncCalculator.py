from random import choice
import networkx as nx


class ObjFuncCalculator:

    @staticmethod
    def random_obj_func(solution, attempt_limit=1000) -> float:
        nodes = list(solution.nodes)
        n_tests = (len(nodes) ** 2) // 2 if len(nodes) <  15 else 100
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

            if t_routes == n_tests:
                break

        if t_routes > 0:
            return t_time / t_routes
        return 0
