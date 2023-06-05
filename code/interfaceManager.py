from singletonMeta import SingletonMeta


class InterfaceManager(metaclass=SingletonMeta):

    def address_selection(self, _list):
        while True:
            msg = f"""
        {_list}
        Selecione um endereço da lista para o teste:

        """
            sel = input(msg)
            sel = int(sel)
            if not 0 <= sel < len(_list):
                print("Valor inválido")
                continue

            msg = """
        Digite o raio da área a ser avaliada:
        """
            radius = input(msg)
            try:
                radius = int(radius)
            except ValueError:
                print("O valor deve ser um inteiro")
                continue

            msg = """
        Digite o orçamento para as alterações:
        """
            budget = input(msg)
            try:
                budget = int(budget)
            except ValueError:
                print("O valor deve ser um inteiro")
                continue


            msg = """
                Digite o tamanho maximo da lista tabu:
                """
            tabu_list_size = input(msg)
            try:
                tabu_list_size = int(tabu_list_size)
            except ValueError:
                print("O valor deve ser um inteiro")
                continue

            return sel, radius, budget, tabu_list_size

    def quit(self):
        msg = """
        ---------------------------------------------------
        """
        print(msg)
