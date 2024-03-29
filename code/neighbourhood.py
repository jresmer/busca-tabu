import osmnx as ox
import concurrent.futures as cf
import copy
from random import choice, sample
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


    def set_log(self, log_manager):
        if isinstance(log_manager, CSVLogManager):
            self.__log = log_manager

    @staticmethod
    def add_lane(solution, u, v, k, max_bool):
        neighbor = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        if 'lanes' not in edge:
            edge['lanes'] = ['1', '1']
        lanes = edge['lanes']
        try:
            if isinstance(lanes, str):
                edge['lanes'] = str(int(lanes) - 1)
            elif max_bool:
                edge['lanes'] = str(int(max(lanes)) + 1)
            else:
                edge['lanes'] = str(int(min(lanes)) + 1)
        except Exception as e:
            pprint(e)
        neighbor[u][v][k]['lanes'] = edge['lanes']
        return neighbor

    @staticmethod
    def remove_lane(solution, u, v, k, max_bool):
        neighbor = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        if 'lanes' not in edge:
            edge['lanes'] = ['1', '1']
        lanes = edge['lanes']
        try:
            if isinstance(lanes, str):
                edge['lanes'] = str(int(lanes) - 1) if int(lanes) > 1 else edge['lanes']
            elif max_bool:
                edge['lanes'] = str(int(max(lanes)) - 1) if int(max(lanes)) > 1 else edge['lanes']
            else:
                edge['lanes'] = str(int(min(lanes)) - 1) if int(min(lanes)) > 1 else edge['lanes']
        except Exception as e:
            pprint(e)
        neighbor[u][v][k]['lanes'] = edge['lanes']
        return neighbor

    def reverse_lane(self, solution, u, v, k):
        neighbor = copy.deepcopy(solution)
        edge = solution.edges[(u, v, k)]
        lanes = edge['lanes'] if 'lanes' in edge else ['1', '1']
        if isinstance(lanes, str) or 'lanes' not in edge:
            if (v, u, k) in [e for e in solution.edges]:
                self.add_lane(solution, v, u, k, False)
                self.remove_lane(solution, u, v, k, False)
            else:
                try:
                    attrs = neighbor[u][v][k]
                    neighbor.remove_edge(u, v, k)
                    neighbor.add_edge(v, u, k)
                    for key in attrs.keys():
                        neighbor[v][u][k][key] = attrs[key]
                except Exception as e:
                    pprint(e)
        elif len(lanes) == 2:
            edge["lanes"][0] = str(int(edge["lanes"][0]) - 1)
            edge["lanes"][1] = str(int(edge["lanes"][1]) + 1)
            neighbor[u][v][k]['lanes'] = edge['lanes']
        return neighbor

    def get_best_neighbor_random(self, solution, budget_left, max_bool):
        solution = ox.add_edge_speeds(solution)
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]

        best_neighbor = solution
        obj_func_value = 9999
        log_text = ''
        cost = 0
        reverse_op = None

        itr = len(edges) // 10
        change_made = False

        for _ in range(itr):
            u, v, k = choice(edges)
            edges.remove((u, v, k))
            values = [0]*3
            changes = [None]*3
            # add a lane:
            neighbor = self.add_lane(solution, u, v, k, max_bool)
            values[0] = self.__obj_calculator.random_obj_func(neighbor)
            changes [0]= neighbor,\
                f'lane added at {(u, v, k)}', 1500, f'lane removed at {(u, v, k)}'
            # remove a lane:
            neighbor = self.remove_lane(solution, u, v, k, max_bool)
            values[1] = self.__obj_calculator.random_obj_func(neighbor)
            changes [1] = neighbor,\
                f'lane removed at {(u, v, k)}', 1000,  f'lane added at {(u, v, k)}'
            # reverse lane:
            neighbor = self.reverse_lane(solution, u, v, k)
            values[2] = self.__obj_calculator.random_obj_func(neighbor)
            changes[2] = neighbor,\
                f'lane reversed at {(u, v, k)}', 500, f'lane reversed at {(u, v, k)}'

            for _ in range(3):
                obj_value = min(values)
                min_value_index = values.index(obj_value)
                _best_neighbor, _log_text, _cost, _reverse_op = changes[min_value_index]

                if _log_text not in self.__tabu_list and obj_value <= obj_func_value and budget_left - cost >= 0:
                    obj_func_value = obj_value
                    best_neighbor = _best_neighbor
                    log_text = _log_text
                    cost = _cost
                    reverse_op = _reverse_op
                    change_made = True
                    break

        if not change_made:
            self.__tabu_list.erase()
            return best_neighbor, 9999, 0

        self.__log.write_on_log(log_text, best_neighbor.number_of_nodes(), best_neighbor.number_of_edges(), obj_func_value)
        self.__tabu_list.update(reverse_op)
        self.__value_list.append(abs(obj_func_value - self.__obj_calculator.random_obj_func(solution)))
        self.__change_list.append(reverse_op)

        return best_neighbor, obj_func_value, cost
    
    def get_neighbors(self, solution, edges, max_bool, itr):
        values = []
        changes = []
        edges = sample(edges, itr)
        for u, v, k in edges:
            # add a lane:
            neighbor = self.add_lane(solution, u, v, k, max_bool)
            values.append(self.__obj_calculator.random_obj_func(neighbor))
            changes.append((neighbor,\
                f'lane added at {(u, v, k)}', 1500, f'lane removed at {(u, v, k)}'))
            # remove a lane:
            neighbor = self.remove_lane(solution, u, v, k, max_bool)
            values.append(self.__obj_calculator.random_obj_func(neighbor))
            changes.append((neighbor,\
                f'lane removed at {(u, v, k)}', 1000,  f'lane added at {(u, v, k)}'))
            # reverse lane:
            neighbor = self.reverse_lane(solution, u, v, k)
            values.append(self.__obj_calculator.random_obj_func(neighbor))
            changes.append((neighbor,\
                f'lane reversed at {(u, v, k)}', 500, f'lane reversed at {(u, v, k)}'))
        
        for _ in range(itr):
            obj_value = min(values)
            min_value_index = values.index(obj_value)
            _best_neighbor, log_text, cost, reverse_op = changes[min_value_index]

            if log_text not in self.__tabu_list:
                break

        return _best_neighbor, log_text, cost, reverse_op, obj_value
    
    def parallel_get_best_neighbor(self, solution, budget_left, max_bool, cores=20):
        solution = ox.add_edge_speeds(solution)
        solution = ox.add_edge_travel_times(solution)
        edges = [e for e in solution.edges]

        best_neighbor = solution
        obj_func_value = self.__obj_calculator.random_obj_func(solution)
        log_text = ''
        cost = 0
        reverse_op = None

        itr = len(edges) // (10 * cores) 
        change_made = False

        with cf.ProcessPoolExecutor(max_workers=cores) as p_executor:
            futures = {p_executor.submit(self.get_neighbors, solution, edges, max_bool, itr)}

            for future in cf.as_completed(futures):
                neighbor, _log_text, _cost, _reverse_op, obj_value = future.result()
                if obj_value < obj_func_value and budget_left - _cost >= 0:
                    best_neighbor = neighbor
                    obj_func_value = obj_value
                    log_text = _log_text
                    cost = _cost
                    reverse_op = _reverse_op
                    change_made = True

            p_executor.shutdown()

        if not change_made:
            self.__tabu_list.erase()
            return best_neighbor, obj_func_value, 0

        self.__log.write_on_log(log_text, best_neighbor.number_of_nodes(), best_neighbor.number_of_edges(), obj_func_value)
        self.__tabu_list.update(reverse_op)
        self.__value_list.append(abs(obj_func_value - self.__obj_calculator.random_obj_func(solution)))
        self.__change_list.append(reverse_op)
        
        return best_neighbor, obj_func_value, cost

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

        d = {'reversed' : 500, "added" : 1000, "removed" : 1500}
        if (u, v, k) not in [e for e in solution.edges]:
            if (v, u, k) in [e for e in solution.edges]:
                u, v = v, u
            else:
                print(f'Edge not found!')
                return solution, d[operation]
        if operation == "reversed":
            solution = self.reverse_lane(solution, u, v, k)
            recovered_budget = 500
        elif operation == "added":
            solution = self.add_lane(solution, u, v, k, max_bool)
            recovered_budget = 1000
        else:
            solution = self.remove_lane(solution, u, v, k, max_bool)
            recovered_budget = 1500
        
        return solution, recovered_budget
