import csv
import time


class CSVLogManager:


    def __init__(self, address, dist, budget):
        city = address.split(", ")
        city = city[1]
        self.__starting_time = time.time()
        self.__filename = f'{city}-log.csv'
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Adress', 'Radius', 'Budget']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Adress' : str(address),
                               'Radius' : str(dist), 'Budget' : str(budget)})
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Operation', 'Number of Nodes', 'Value', 'Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

    def write_on_log(self, operation, num_nodes, solution_value):
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Operation', 'Number of Nodes', 'Value', 'Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({'Operation' : operation, 'Number of Nodes' : str(num_nodes),
                              'Value' : str(solution_value), 'Time' : str(time.time() - self.__starting_time)})

    def quit(self, status=''):
        with open(self.__filename, 'a', newline='') as csv_file:
            fieldnames = ['Status', 'Ending Time']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'Status' : status, 'Ending Time' : str(time.time() - self.__starting_time)})

