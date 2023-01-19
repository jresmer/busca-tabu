from random import randint
import networkx as nx


class ObjFuncCalculator:

    def obj_func_radom(self, solution, num_tests=100, attempt_limit=10000) -> float:
        node_list = list(solution.nodes)
        pairs = []
        for node1 in node_list:
            for node2 in node_list:
                if nx.has_path(solution, node1, node2):
                    pairs.append((node1, node2))

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
