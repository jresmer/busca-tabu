from datetime import datetime


class LogManager:

    def __init__(self, steps):
        self.__start_time = datetime.now()
        self.__counter = 0
        self.__steps_for_first_solution = steps
        self.__log_name = f'log-d:{datetime.now()}.txt'
        log_text = f'Time: {self.__start_time}'
        f = open(self.__log_name, 'a')
        f.write(log_text)
        f.close()

    def write_on_log(self, operation, num_nodes, solution_value):
        self.__counter += 1
        log_text = f"""
-------------------------------------------------
Time: {datetime.now()}
Operation: {operation}
Number of nodes in the solution: {num_nodes}
Solution's value: {solution_value}

"""
        f = open(self.__log_name, 'a')
        f.write(log_text)
        f.close()

    def quit(self, status=''):
        log_text = f'Session ended at time: {datetime.now()}{status}, operations made: {self.__counter - self.__steps_for_first_solution}'
        log_text = "\n" + f'{log_text}' + "\n" + "\n"
        f = open(self.__log_name, 'a')
        f.write(log_text)
        f.close()
