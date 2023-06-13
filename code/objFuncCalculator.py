from random import choice
from random import sample
import networkx as nx
import concurrent.futures as cf


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
    
        @staticmethod
        def __time_step(solution, pair):
            if (pair[0], pair[1]) in self.__tested_pairs: return 0

            self.__tested_pairs.append((pair[0], pair[1]))

            shortest_path_length = nx.shortest_path_length(solution, pair[0],
                                                           pair[1], weight='travel_time')
            
            return shortest_path_length
        
        def parallel_random_obj_func(self, solution, num_tests):
            with cf.ProcessPoolExecutor() as pool_executor:
                edges = [e for e in solution.edges]
                edges_ = sample(edges, num_tests)
                futures = {pool_executor.submit(self.__time_step, edge) for edge in edges_}

                total_time = 0
                for future in cf.as_completed(futures):
                    total_time += future.result()

                pool_executor.shutdown()

            self.__tested_pairs = []

            return total_time / num_tests
