from random import choice
import networkx as nx


class ObjFuncCalculator:

    def obj_func_random(self, solution, num_tests=100, attempt_limit=10000) -> float:
        node_list = list(solution.nodes)
        self.pair_list = []

        t_routes = 0
        t_time = 0

        while attempt_limit > 0:
            length = len(node_list) - 1
            if length == -1:
                break

            origin = choice(node_list)
            dest = choice(node_list)

            if origin == dest or (origin, dest) in self.pair_list:
                continue

            self.pair_list.append((origin, dest))

            if not nx.has_path(solution, origin, dest):
                continue

            shortest_path_length = nx.shortest_path_length(solution, origin, dest,
                                                           weight='travel_time')

            if shortest_path_length != 0:
                t_time += shortest_path_length
                t_routes += 1

            if t_routes == num_tests:
                break

        if t_routes > 0:
            return t_time / t_routes
        return 0
