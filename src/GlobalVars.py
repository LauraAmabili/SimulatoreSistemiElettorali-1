class HubClass:

    def get_subdivisions(self, sup, sub_name):
        """
        sup: o un'istanza di una geoEnt, o una tupla (nomeClasse, nomeIstanza)
        sub_name: nome classe target

        return: list of names (stringhe)
        """
        pass

    def get_superdivision(self, sub, sup_name):
        """
        sub: o un'istanza o una tuple
        sup_name: nome classe target

        return nome istanza target
        """
        pass

    def get_instance(self, class_name, inst_name):
        pass

    def add_subdiv(self, sup_type, sub_type, var_name):
        """
        Records that instances of sup_type have instances of sub_type stored in self.var_name
        """

Hub = HubClass()
