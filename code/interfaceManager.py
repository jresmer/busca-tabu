class InterfaceManager:

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





    def quit(self):
        msg = """
        
        """
        print(msg)
