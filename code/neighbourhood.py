import osmnx as ox
import copy
from random import choice
from tabuList import TabuList
from pprint import pprint
from objFuncCalculator import ObjFuncCalculator
from logManager import LogManager
from singletonMeta import SingletonMeta


class Neighbourhood(metaclass=SingletonMeta):

    def __init__(self, tabu_list=TabuList()):
        self.__obj_calculator = ObjFuncCalculator()
        self.__tabu_list = tabu_list
        self.__log = None
        self.__operations = {'add': self.__add_lane, 'remove': self.__remove_lane, 'reverse': self.__reverse_lane}

    def set_log(self, log_manager):
        if isinstance(log_manager, LogManager):
            self.__log = log_manager

    @staticmethod
    def __add_lane(solution, u, v, k, max_bool):
        neighbour = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        lanes = edge['lanes'] if 'lanes' in edge else ['1', '1']
        try:
            if isinstance(lanes, str):
                edge['lanes'] = str(int(lanes) - 1)
            elif max_bool:
                edge['lanes'] = str(int(max(lanes)) + 1)
            else:
                edge['lanes'] = str(int(min(lanes)) + 1)
        except Exception as e:
            pprint(e)
        neighbour[u][v][k]['lanes'] = edge['lanes']
        neighbour = ox.add_edge_travel_times(neighbour)
        return neighbour

    @staticmethod
    def __remove_lane(solution, u, v, k, max_bool):
        neighbour = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        lanes = edge['lanes'] if 'lanes' in edge else ['1', '1']
        if lanes != '1':
            try:
                if isinstance(lanes, str):
                    edge['lanes'] = str(int(lanes) - 1)
                elif max_bool:
                    edge['lanes'] = str(int(max(lanes)) - 1)
                else:
                    edge['lanes'] = str(int(min(lanes)) - 1)
            except Exception as e:
                pprint(e)
        neighbour[u][v][k]['lanes'] = edge['lanes']
        neighbour = ox.add_edge_travel_times(neighbour)
        return neighbour

    @staticmethod
    def __reverse_lane(solution, u, v, k):
        neighbour = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        lanes = edge['lanes'] if 'lanes' in edge else ['1', '1']
        if isinstance(lanes, str) or len(lanes) == 1:
            try:
                attrs = neighbour[u][v][k]
                neighbour.remove_edge(u, v, k)
                neighbour.add_edge(v, u, k)
                for key in attrs.keys():
                    neighbour[v][u][k][key] = attrs[key]
            except Exception as e:
                pprint(e)
        elif len(lanes) == 2:
            edge["lanes"][0] = int(edge["lanes"][0]) - 1
            edge["lanes"][1] = int(edge["lanes"][1]) + 1
            neighbour[u][v][k]['lanes'] = edge['lanes']
        return neighbour

    def get_best_neighbour_random(self, solution, budget_left, max_bool):
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]

        best_neighbour = solution
        obj_func_value = 10000
        log_text = ''
        cost = 0
        reverse_op = None

        itr = len(edges) // 10

        for _ in range(itr):
            u, v, k = choice(edges)
            edges.remove((u, v, k))
            dictio = {}
            # add a lane:
            neighbour = self.__add_lane(solution, u, v, k, max_bool)
            if neighbour not in self.__tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour,\
                    f'lane added at {(u, v, k)}', 1500, f'lane removed at {(u, v, k)}'
            # remove a lane:
            neighbour = self.__remove_lane(solution, u, v, k, max_bool)
            if neighbour not in self.__tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour,\
                    f'lane removed at {(u, v, k)}', 1000,  f'lane add at {(u, v, k)}'
            # reverse lane:
            neighbour = self.__reverse_lane(solution, u, v, k)
            if neighbour not in self.__tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour,\
                    f'lane reversed at {(u, v, k)}', 500, f'lane reversed at {(u, v, k)}'

            if len(dictio) == 0:
                continue
            for i in range(3):
                neighbour_list = list(dictio.keys())
                neighbour_list.sort()
                obj_value = neighbour_list[0]
                _best_neighbour, log_text, cost, reverse_op = dictio[obj_value]

                if log_text not in self.__tabu_list and obj_value <= obj_func_value and budget_left - cost > 0:
                    obj_func_value = obj_value
                    best_neighbour = _best_neighbour
                    break

        self.__log.write_on_log(log_text, best_neighbour.number_of_nodes(), obj_func_value)
        self.__tabu_list.update(reverse_op)

        return best_neighbour, obj_func_value, cost

    def random_neighbour(self, solution, max_bool=False):
        solution = ox.add_edge_speeds(solution)
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges.keys()]
        u, v, k = choice(edges)
        _operation = choice(list(self.__operations.keys()))
        if _operation == 'reverse':
            solution = self.__operations[_operation](solution, u, v, k)
        else:
            solution = self.__operations[_operation](solution, u, v, k, max_bool)

        self.__log.write_on_log(f'{_operation} at {(u, v, k)}', solution.number_of_nodes(),
                                self.__obj_calculator.obj_func_random(solution))

        return solution
