from neighbourhood import Neighbourhood
from tabuList import TabuList
import networkx as nx


class TabuSearch:

    def __init__(self):
        self.s = self.get_first_solution()
        self.best_solution = self.s
        self.opt_value = self.obj_function(self.s)
        self.tabu_list = TabuList()

    def get_first_solution(self) -> nx.classes.multidigraph.MultiDiGraph:
        pass

    def obj_function(self, solution) -> int:
        pass

    def loop(self):
        for _ in range(50):
            nd = Neighbourhood(self.s)
            opt_nb = nd.neighbourhood[0]
            value = self.obj_function(opt_nb)

            for _s in nd.neighbourhood:
                _value = self.obj_function(_s)
                if _s not in self.tabu_list and _value < value:
                    value = _value
                    opt_nb = _s

            if self.opt_value >= value:
                self.best_solution = opt_nb

            self.tabu_list.update(self.s)
            self.s = opt_nb
