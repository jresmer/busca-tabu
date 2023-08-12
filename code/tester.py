from tabuSearch import TabuSearch
from solutionDAO import SolutionDAO


class Tester:

    @staticmethod
    def run_test():
        dao = SolutionDAO()
        for dist in [500, 1500]:
            for budget in [30000, 80000, 130000]:
                for tabu_list_size in [20, 40, 80]:
                    for itr in [50, 75]:
                        tabu_search = TabuSearch()
                        tabu_search.run(0, dist, budget, tabu_list_size, itr=itr)
                        dao.add(tabu_search.get_best_solution())
