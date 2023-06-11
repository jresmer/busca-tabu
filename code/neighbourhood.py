import osmnx as ox
import copy
from random import choice
from tabuList import TabuList
from pprint import pprint
from objFuncCalculator import ObjFuncCalculator
from csvLogManager import CSVLogManager
from singletonMeta import SingletonMeta


class Neighbourhood(metaclass=SingletonMeta):

    def __init__(self, tabu_list_size: int):
        self.__obj_calculator = ObjFuncCalculator()
        self.__tabu_list = TabuList(tabu_list_size)
        self.__value_list = []
        self.__change_list = []
        self.__log = None
        self.__operations = {'added': self.__add_lane, 'removed': self.__remove_lane, 'reversed': self.__reverse_lane}


    def set_log(self, log_manager):
        if isinstance(log_manager, CSVLogManager):
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
        if isinstance(lanes, str) or 'lanes' not in edge:
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
        solution = ox.add_edge_speeds(solution)
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]

        best_neighbour = solution
        obj_func_value = 9999
        log_text = ''
        cost = 0
        reverse_op = None

        itr = len(edges) // 10
        change_made = False

        for _ in range(itr):
            u, v, k = choice(edges)
            edges.remove((u, v, k))
            values = []
            changes = []
            # add a lane:
            neighbour = self.__add_lane(solution, u, v, k, max_bool)
            values[0] = self.__obj_calculator.obj_func_random(neighbour)
            changes [0]= neighbour,\
                f'lane added at {(u, v, k)}', 1500, f'lane removed at {(u, v, k)}'
            # remove a lane:
            neighbour = self.__remove_lane(solution, u, v, k, max_bool)
            values[1] = self.__obj_calculator.obj_func_random(neighbour)
            changes [1] = neighbour,\
                f'lane removed at {(u, v, k)}', 1000,  f'lane added at {(u, v, k)}'
            # reverse lane:
            neighbour = self.__reverse_lane(solution, u, v, k)
            values[2] = self.__obj_calculator.obj_func_random(neighbour)
            changes[2] = neighbour,\
                f'lane reversed at {(u, v, k)}', 500, f'lane reversed at {(u, v, k)}'

            for i in range(3):
                obj_value = min(values)
                min_value_index = values.index(obj_value)
                _best_neighbour, log_text, cost, reverse_op = changes[min_value_index]

                if log_text not in self.__tabu_list and obj_value <= obj_func_value and budget_left - cost >= 0:
                    obj_func_value = obj_value
                    best_neighbour = _best_neighbour
                    change_made = True
                    break

        if not change_made:
            self.__tabu_list.erase()

        self.__log.write_on_log(log_text, best_neighbour.number_of_nodes(), obj_func_value)
        self.__tabu_list.update(reverse_op)
        self.__value_list.append(abs(obj_func_value - self.__obj_calculator.obj_func_random(solution)))
        self.__change_list.append(reverse_op)

        return best_neighbour, obj_func_value, cost

    def reverse_change(self, solution, max_bool=False):
        solution = ox.add_edge_speeds(solution)
        solution = ox.add_edge_travel_times(solution)

        value = min(self.__value_list)
        index = self.__value_list.index(value)
        self.__value_list.pop(index)
        operation = self.__change_list.pop(index)
        operation = operation.split()
        operation, edges = operation[1], operation[3] + operation[4] + operation[5]
        edges = edges.split(",")
        recovered_budget = 0

        u, v, k = int(edges[0][1:]), int(edges[1]), int(edges[2][:-1])

        if operation == "reversed":
            if (u, v, k) not in [e for e in solution.edges]:
                if (v, u, k) in [e for e in solution.edges]:
                    u, v = v, u
                else:   # edge no longer exists
                    return solution, 500
            solution = self.__operations[operation](solution, u, v, k)
            recovered_budget = 500
        else:
            if (u, v, k) not in [e for e in solution.edges]:
                if (v, u, k) in [e for e in solution.edges]:
                    u, v = v, u
                elif operation == "added":
                    solution.add_edge(u, v)
                    solution = ox.add_edge_speeds(solution)
                    solution = ox.add_edge_travel_times(solution)
                else:   # edge no longer exists
                    return solution, 1000
            solution = self.__operations[operation](solution, u, v, k, max_bool)
            if operation == "added":
                recovered_budget = 1000
            else:
                recovered_budget = 1500
        
        return solution, recovered_budget
