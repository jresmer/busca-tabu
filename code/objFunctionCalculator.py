from random import randint
import networkx as nx
import threading as td


class ObjectiveFunctionCalculator:

    def obj_function_random(self, solution, num_tests=100, attempt_limit=10000) -> float:
        self.__t_time = 0
        self.__t_routes = 0
        self.__pair_list = []
        self.__solution = solution
        self.__num_tests = num_tests
        self.__attempt_limit = attempt_limit
        node_list = list(solution.nodes)
        length = len(node_list)

        thread_1 = td.Thread(target=self.geb_path_time, args=node_list[0: length // 4 + 1])
        thread_2 = td.Thread(target=self.geb_path_time, args=node_list[length // 4 + 1: length // 2 + 1])
        thread_3 = td.Thread(target=self.geb_path_time, args=node_list[length // 2 + 1: length * 3 // 4 + 1])
        thread_4 = td.Thread(target=self.geb_path_time, args=node_list[length * 3 // 4 + 1: length])
        threads = [thread_4, thread_3, thread_2, thread_1]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if self.__t_routes > 0:
            return self.__t_time / self.__t_routes
        return 0

    def geb_path_time(self, node_list):
        while self.__attempt_limit > 0:
            length = len(node_list) - 1
            if length == -1:
                break

            origin_index = randint(0, length)
            dest_index = randint(0, length)

            if origin_index == dest_index or (origin_index, dest_index) in self.__pair_list:
                continue

            self.__pair_list.append((origin_index, dest_index))

            origin, dest = node_list[origin_index], node_list[dest_index]

            if not nx.has_path(self.__solution, origin, dest):
                continue

            shortest_path_length = nx.shortest_path_length(self.__solution, origin, dest,
                                                           weight='travel_time')

            if shortest_path_length != 0:
                self.__t_time += shortest_path_length
                self.__t_routes += 1

            if self.__t_routes == self.__num_tests:
                break
