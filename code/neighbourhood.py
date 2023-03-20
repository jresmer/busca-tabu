import osmnx as ox
import copy
from random import choice
from tabuList import TabuList
from pprint import pprint
from objFuncCalculator import ObjFuncCalculator
from logManager import LogManager
from singletonMeta import SingletonMeta


class Neighbourhood(metaclass=SingletonMeta):

    def __init__(self):
        self.__neighbourhood = []
        self.__obj_calculator = ObjFuncCalculator()
        self.__operations = {'add': self.add_lane, 'remove': self.remove_lane, 'reverse': self.reverse_lane}

    @property
    def neighbourhood(self):
        return self.__neighbourhood

    @staticmethod
    def add_lane(solution, u, v, k, max_bool):
        neighbour = copy.deepcopy(solution)
        edge = neighbour.edges[(u, v, k)]
        lanes = edge['lanes'] if 'lanes' in edge else '1'
        try:
            if max_bool:
                edge['lanes'] = str(int(max(lanes) + 1))
            else:
                edge['lanes'] = str(int(min(lanes) + 1))
        except Exception as e:
            pprint(e)
        neighbour[u][v][k]['lanes'] = edge['lanes']
        neighbour = ox.add_edge_travel_times(neighbour)
        return neighbour

    @staticmethod
    def remove_lane(solution, u, v, k, max_bool):
        neighbour = copy.deepcopy(solution)
        edge = neighbour.edges[(u, v, k)]
        lanes = edge['lanes']
        if lanes != '1':
            try:
                if max_bool:
                    edge['lanes'] = str(int(max(lanes)) - 1)
                else:
                    edge['lanes'] = str(int(min(lanes)) - 1)
            except Exception as e:
                pprint(e)
        neighbour[u][v][k]['lanes'] = edge['lanes']
        neighbour = ox.add_edge_travel_times(neighbour)
        return neighbour

    @staticmethod
    def reverse_lane(solution, u, v, k):
        neighbour = copy.deepcopy(solution)
        edge = neighbour.edges[(u, v, k)]
        if len(edge['lanes']) == 1:
            try:
                attrs = neighbour[u][v][k]
                neighbour.remove_edge(u, v, k)
                neighbour.add_edge(v, u, k)
                for key in attrs.keys():
                    neighbour[v][u][k][key] = attrs[key]
            except Exception as e:
                pprint(e)
        elif len(edge['lanes']) == 2:
            edge["lanes"][0] = int(edge["lanes"][0]) - 1
            edge["lanes"][1] = int(edge["lanes"][1]) + 1
            neighbour[u][v][k]['lanes'] = edge['lanes']
        return neighbour

    def get_best_neighbour_random(self, solution, budget_left, max_bool, num_it, tabu_list=TabuList()):
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]

        best_neighbour = None
        obj_func_value = 10000
        log_text = ''

        for _ in range(num_it):
            u, v, k = choice(edges)
            dictio = {}
            # add a lane:
            neighbour = self.add_lane(solution, max_bool, u, v, k)
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour, f'lane added at {(u, v, k)}', 1500
            # remove a lane:
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour, f'lane removed at {(u, v, k)}', 1000
            # reverse lane:
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_random(neighbour)] = neighbour, f'lane reversed at {(u, v, k)}', 500

            if len(dictio) == 0:
                continue

            neighbour_list = list(dictio.keys())
            neighbour_list.sort()
            obj_value = neighbour_list[0]
            _best_neighbour, log_text, cost = dictio[obj_value]

            if obj_value <= obj_func_value and budget_left - cost > 0:
                obj_func_value = obj_value
                best_neighbour = _best_neighbour
                log_text = "\n" + f'{log_text}' + "\n" + "\n"

        LogManager().write_on_log(log_text, best_neighbour.number_of_nodes())

        return best_neighbour, obj_func_value, cost

    def random_neighbour(self, solution, max_bool=False):
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]
        u, v, k = choice(edges)
        _operation = choice(list(self.__operations.keys()))
        if _operation == 'reverse':
            solution = self.__operations[_operation](solution, u, v, k)
        else:
            solution = self.__operations[_operation](solution, u, v, k, max_bool)

        return solution
