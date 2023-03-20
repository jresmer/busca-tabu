from time import time


from singletonMeta import SingletonMeta


class LogManager(metaclass=SingletonMeta):

    def __init__(self):
        self.__start_time = time()
        log_text = f'Time: {self.__start_time}'
        f = open('log.txt', 'w')
        f.write(log_text)
        f.close()

    def write_on_log(self, operation, num_nodes):
        log_text = f"""
-------------------------------------------------
Time: {time()}
Operation: {operation}
Number of nodes in the solution: {num_nodes}

"""
        f = open('log.txt', 'w')
        f.write(log_text)
        f.close()

    def quit(self):
        log_text = f'Session ended at time: {time()}'
        log_text = "\n" + f'{log_text}' + "\n" + "\n"
        f = open('log.txt', 'w')
        f.write(log_text)
        f.close()
