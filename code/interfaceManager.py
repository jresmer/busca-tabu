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
            except:
                print("O valor deve ser um inteiro")
                continue

            msg = """
        Digite o número de iterações executadas ao gerar uma solução inicial:
        """
            steps = input(msg)
            try:
                steps = int(steps)
            except:
                print("O valor deve ser um inteiro")
                continue

            msg = """
        Digite o orçamento para as alterações:
        """
            budget = input(msg)
            try:
                budget = int(budget)
            except:
                print("O valor deve ser um inteiro")
                continue

            return sel, radius, steps, budget

    def quit(self):
        msg = """
        ---------------------------------------------------
        """
        print(msg)
