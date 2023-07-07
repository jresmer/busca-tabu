from tabuSearch import TabuSearch
from solutionDAO import SolutionDAO


class Tester:

    @staticmethod
    def run_test():
        dao = SolutionDAO()
        for address_sel in [0, 1, 2]:
            for dist in [500, 1500, 4500]:
                for budget in [30000, 80000, 130000]:
                    for tabu_list_size in [20, 40, 80]:
                        tabu_search = TabuSearch()
                        tabu_search.run(address_sel, dist, budget, tabu_list_size)
                        dao.add(tabu_search.get_best_solution())
