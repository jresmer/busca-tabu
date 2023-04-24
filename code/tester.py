from tabuSearch import TabuSearch


class Tester:

    @staticmethod
    def run_test():
        for address_sel in [0, 1, 2, 3]:
            for dist in [500, 1000, 1500, 2000]:
                for steps in [10, 20, 30, 50, 80, 130]:
                    for budget in [10000, 20000, 30000, 80000, 130000]:
                        for perc in [5, 10, 20]:
                            tabu_search = TabuSearch()
                            tabu_search.run(address_sel, dist, steps, budget, perc)

