import pickle
from networkx import MultiDiGraph


class SolutionDAO:

    def __init__(self):
        self.__data = []
        self.__file = "solutions_data.txt"
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        with open(self.__file, "wb") as file:
            pickle.dump(self.__data, file)

    def __load(self):
        with open(self.__file, "rb") as file:
            self.__data = pickle.load(file)

    def add(self, solution: MultiDiGraph):
        self.__data.append(solution)
        self.__dump()

    def get(self, key):
        try:
            return self.__data[key]
        except KeyError as e:
            print(e)

    def get_all(self):
        return self.__data

    def clear(self):
        self.__data = []
        self.__dump()
