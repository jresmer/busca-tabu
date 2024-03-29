import csv
import time


class CSVLogManager:


    def __init__(self, address, dist, budget, tabu_list_size, itr):
        city = address.split(", ")
        city = city[1]
        self.__starting_time = time.time()
        self.__filename = f'{city}-log.csv'
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Adress', 'Radius', 'Budget', "Tabu List's Max Size", "n_itr"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Adress' : str(address), 'Radius' : str(dist),
                                'Budget' : str(budget), "Tabu List's Max Size" : str(tabu_list_size),
                                "n_itr" : str(itr)})
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Operation', 'Number of Nodes', 'Number of Edges', 'Value', 'Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def write_on_log(self, operation, n_nodes, n_edges, solution_value):
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Operation', 'Number of Nodes', 'Number of Edges', 'Value', 'Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Operation' : operation, 'Number of Nodes' : str(n_nodes), 'Number of Edges' : str(n_edges),
                              'Value' : str(solution_value), 'Time' : str(time.time() - self.__starting_time)})

    def quit(self, status='None'):
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Status', 'Ending Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Status' : status, 'Ending Time' : str(time.time() - self.__starting_time)})

