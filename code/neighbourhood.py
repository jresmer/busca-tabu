import networkx as nx
import osmnx as ox
import copy
from tabuList import TabuList
from pprint import pprint


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

    @property
    def neighbourhood(self):
        return self.__neighbourhood

    def get_best_neighbour(self, solution, tabu_list):
        pass

    def generate_neighbourhood(self, solution, tabu_list=TabuList(), max_bool=False):
        solution = ox.add_edge_travel_times(solution)
        edges = solution.edges(keys=True, data=True)
        for u, v, k, data in edges:
            # add a lane:
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
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)
            # remove a lane:
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
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)
            # reverse lane:
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
            # add to neighbourhood:
            if neighbour not in tabu_list:
                self.__neighbourhood.append(neighbour)
