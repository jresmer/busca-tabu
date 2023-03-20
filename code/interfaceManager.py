from singletonMeta import SingletonMeta


class InterfaceManager(metaclass=SingletonMeta):

    def address_selection(self, _list):
        while True:
            msg = f"""
        {_list}
        Selecione um endereço da lista para o teste:
        
        """
            sel = input(msg)
            if 0 <= int(sel) < len(_list):
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

            msg = """
            :
            """
            max_bool = input(msg)
            if max_bool == '1':
                max_bool = True
            elif max_bool == '0':
                max_bool = False
            else:
                print("O valor deva ser um inteiro do intervalo [0, 1]")
                continue

            return sel, radius, steps, budget, max_bool

    def quit(self):
        msg = """
        ---------------------------------------------------
        """
        print(msg)
