from datetime import datetime
# from singletonMeta import SingletonMeta


class LogManager:

    def __init__(self, steps):
        self.__start_time = datetime.now()
        self.__counter = 0
        self.__steps_for_first_solution = steps
        log_text = f'Time: {self.__start_time}'
        f = open('log.txt', 'w')
        f.write(log_text)
        f.close()

    def write_on_log(self, operation, num_nodes):
        self.__counter += 1
        log_text = f"""
-------------------------------------------------
Time: {datetime.now()}
Operation: {operation}
Number of nodes in the solution: {num_nodes}

"""
        f = open('log.txt', 'a')
        f.write(log_text)
        f.close()

    def quit(self, status=''):
        log_text = f'Session ended at time: {datetime.now()}{status}, operations made: {self.__counter - self.__steps_for_first_solution}'
        log_text = "\n" + f'{log_text}' + "\n" + "\n"
        f = open('log.txt', 'a')
        f.write(log_text)
        f.close()
