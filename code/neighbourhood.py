import osmnx as ox
import copy
from tabuList import TabuList
from pprint import pprint
from objFuncCalculator import ObjFuncCalculator


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

            return cls._instances[cls]


class Neighbourhood(metaclass=SingletonMeta):

    def __init__(self):
        self.__neighbourhood = []
        self.__obj_calculator = ObjFuncCalculator()

    @property
    def neighbourhood(self):
        return self.__neighbourhood

    def add_lane(self, solution, max_bool, u, v, k):
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

    def remove_lane(self, solution, max_bool, u, v, k):
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

    def reverse_lane_(self, solution, u, v, k):
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

    def generate_neighbourhood(self, solution, tabu_list=TabuList(), max_bool=False):
        solution = ox.add_edge_travel_times(solution)
        edges = solution.edges(keys=True, data=True)
        for u, v, k, data in edges:
            # add a lane:
            neighbour = self.add_lane(solution, max_bool, u, v, k)
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)
            # remove a lane:
            neighbour = self.remove_lane(solution, max_bool, u, v, k)
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)
            # reverse lane:
            neighbour = self.reverse_lane_(solution, u, v, k)
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)

    def get_best_neighbour(self, solution, tabu_list=TabuList(), max_bool=False):
        solution = ox.add_edge_travel_times(solution)
        edges = solution.edges(keys=True, data=True)

        best_neighbour = None
        obj_func_value = 10000

        for u, v, k, data in edges:
            dictio = {}
            # add a lane:
            neighbour = self.add_lane(solution, max_bool, u, v, k)
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_radom(neighbour)] = neighbour
            # remove a lane:
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_radom(neighbour)] = neighbour
            # reverse lane:
            if neighbour not in tabu_list:
                dictio[self.__obj_calculator.obj_func_radom(neighbour)] = neighbour

            if len(dictio) == 0:
                continue

            neighbour_list = list(dictio.keys())
            neighbour_list.sort()
            obj_value = neighbour_list[0]

            if obj_value <= obj_func_value:
                obj_func_value = obj_value
                best_neighbour = dictio[obj_value]

        return best_neighbour
