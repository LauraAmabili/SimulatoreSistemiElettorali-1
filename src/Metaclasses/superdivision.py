# -*- coding: utf-8 -*-
import pandas as pd
import src.GlobalVars

from src import Commons
commons = Commons

class superdivision(type):
    """
    This metaclass handles the aspects of a geoEnt related to it having lower levels under it.
    In particular I will have to tell the class to what information from the lower classes it has access to,
    in the class creation process I'll also be telling the Hub about the relationship

    In the configuration, for each lower class I'll be telling:
        + in which variable the list of names will be stored (this will be the key of the dict)
        + the type of the lower class
        + the functions/parameters I want to expose

    TODO: !!!! IDEA: !!!!
    Use source to define the function to call, it'll return a function which you'll need to call providing 'locals'.

    When the proxy function (the one defined by superdivision) is called this will allow you to forward the arguments.

    For each subdivision in the list I'll create a fake local_namespace where self is mapped to a reference of the
    subdivision.

    This way I can make use of the source syntax seamlessly

    TODO: for each subdivision add an ini

    """
    def __new__(mcs, *args, subdivisions=None, **kwargs):

        """
        Questa metaclasse deve essere prima di external,
        """
        # print("Superdivision configuration: ", subdivisions)

        if subdivisions is None:
            return super().__new__(mcs, *args, **kwargs)

        dict_external = kwargs.get("external", {})
        for name, info in subdivisions.items():
            # aggiungi queste variabili a quelle da mettere nell'init
            dic_existant = dict_external.get(name, {})
            dic_existant['init'] = True
            dict_external[name] = dic_existant

            # aggiungi ad Hub
            src.GlobalVars.Hub.add_subdiv(args[0], info['type'], name)

            # functions ha una lista di dizionari {name: nome_funz, source: <funzione>}
            for i in info['functions']:
                args[2][f"subs_{name}_{i['name']}"] = superdivision.generate_accessor(info['type'],
                                                                               i['source'])

        kwargs['external'] = dict_external
        # print("After superdivision: ", args, kwargs)
        return super().__new__(mcs, *args, **kwargs)

    @staticmethod
    def generate_accessor(classe_oggetti, source):
        """
        + nome_funzione: diventerà subs_nome_funzione
        + classe_oggetti: es: Circoscrizione
        + source: funzione che deve essere chiamata come: source(locals(), *args, **kwargs)

        Restituisce una funzione che prende:
            + self
            + *args
            + **kwargs

        La funzione restituita verrà aggiunta al dizionario che viene passato a type con chiave: subs_nome_funzione
        """
        def accessor(self, *args, **kwargs):
            lis_obj = src.GlobalVars.Hub.get_subdivisions(self, classe_oggetti, instance=True)
            # print("sup_accessor: ", lis_obj)
            # print("source: ", source)
            lis_res = [source({'self':s, 'commons':Commons, 'Commons':Commons}, *args, **kwargs) for s in lis_obj]
            # list(map(lambda s: source()({'self':s}, *args, **kwargs), lis_obj))
            if type(lis_res[0]) == int:
                res = sum(lis_res)
            elif type(lis_res[0]) == pd.DataFrame:
                res = pd.concat(lis_res, ignore_index=True)
            else:
                res = lis_res
            return res

        return accessor

    @staticmethod
    def parse_conf(configuration):
        return configuration
