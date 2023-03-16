from time import time


class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


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
