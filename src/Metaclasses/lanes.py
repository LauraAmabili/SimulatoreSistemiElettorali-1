# -*- coding: utf-8 -*-
"""
Tutti i membri di una lane sanno quanti rappresentanti vengono eletti ai livelli inferiori (funzione to_elect che è
ricorsiva con caso base in lane_bottom)

All must provide the functions:
    + is_lane_endpoint([type])

lane_head e lane_middle hanno riferimenti al livelli inferiore, solo un livello inferiore può essere indicato. Deve
essere indicato nel seguente modo:
sub1.sub2. ... .subT::Target, questa notazione si traduce in:
    > scegli le subdivision nella lista sub1, per ognuna scegli le subdivision nella lista sub2 degli elementi di
    sub1 e così via fino alla lista subT degli elementi di subN che avranno tipo target.
    > Se l'uninominale fosse una lane che inizia in Nazione e ha solo Uninominale sarebbe:
    > circoscrizioni.plurinominali.uninominali::Uninominale
"""
# TODO: the lane process starting in the lane_head should return a set of strings where the strings are the identifiers
# of the candidates which received a proposal by the lane
# the lane should also, as an intentional side effect, provide each proposed candidate with the information it needs
# to make a choice and to pass down the choice

import itertools
from functools import partial


class FuncList:
    """
    Starts with a list of functions, on call it will apply the argument to the first function,
    then the result to the second and so on
    """

    def __init__(self, funcs):
        self.functions = funcs

    def __call__(self, val):
        r = val
        for i in self.functions:
            r = i(r)
        return r


def gen_func(path):  # var1.var2..
    lis = []
    for i, n in enumerate(path.split('.')):
        lis.append(partial(lambda ns, ls: list(itertools.chain(*map(lambda t: getattr(t, ns, None), ls))), n))
    return FuncList(lis)

def gen_is_lane_endpoint(args, lanes, value):
    old_endpoint = args[2].get('is_lane_endpoint', lambda *s, **kargs: False)

    def is_lane_endpoint(self, lane_name):
        """Checks whether the node is the endpoint of the given lane"""
        if lane_name in lanes:
            return value
        else return old_endpoint(self, lane_name)

    return is_lane_endpoint


class lane_head(type):
    """
    La configurazione di lane_head DEVE indicare un numero prioritario, le lane saranno eseguite in sequenza dando
    priorità a numeri più bassi

    Il punto di partenza della Lane, per esempio nazione. Salvato in hub
    Sa solo correggere le proposte ottenute e calcolare un exact_value
    """

    def __new__(cls, *args, lane_head_args, **kwargs):
        """
        I parametri sono in lane_head ed è un dizionario
        del tipo:
            lane1:
                par1:...
                par2:...
            lane2:
                par2:...
                par3:...
        Parametri:
            sub_div -> la classe che sta sotto nella lane, notazione: sub1.sub2. ... .subT::Target
            apportionment_func -> la funzione da usare per assegnare la divisione dei seggi
                :: subdivision -> input della redistribution
            redistribution_func -> la funzione che aggiusta le stime dei livelli inferiori
                :: caller, lane, subdivisions, ideal distribution -> candidati che hanno ricevuto una proposta
        """

        # Step 1: flip the arguments
        params = dict()
        for l_n, ps in lane_head_args.items():
            for k in ps:
                if k not in params:
                    params[k] = dict()
                params[k][l_n] = ps[k]

        # ----------------------- is_lane_endpoint(lane)
        args[2]['is_lane_endpoint'] = gen_is_lane_endpoint(args, lane_head_args.keys(), False)

        # ----------------------- get_lane_sub('lane')
        def gen_get_lane_sub(args, sub_divs):
            old_get = args[2].get('get_lane_sub', lambda *s,**kargs: [])
            diz_subs = dict()
            diz_type = dict()
            for ln, sub_n in subs.items():
                path, name = sub_n.split('::')
                diz_subs[ln] = gen_func(path)
                diz_type[ln] = name

            def get_lane_sub(self, lane):
                if lane in diz_subs.keys():
                    res = dis_subs[tipo](self)
                    all([]


        subs = params['sub_div']
        old_get = args[2].get('get_lane_sub', lambda *s, **kargs: [])

        diz_subs = dict()
        for ln, sub_n in subs.items():
            path, name = sub_n.split('::')
            diz_subs[ln] = gen_func(path)

        def get_lane_sub(self, tipo):  # attenzione a funzione preesistente, vedi come per il "check end"
            if tipo in diz_subs.keys():
                return diz_subs[tipo](self)  # Chiama la lambda dandogli self
            else:
                return old_get(self, tipo)

        args[2]['get_lane_sub'] = get_lane_sub

        # ----------------------- start_lane('lane')
        apps = params['apportionment_func']
        reds = params['redistribution_func']

        def start_lane(self, lane):
            raise KeyError("No such lane exists")

        if 'start_lane' in args[2]:
            start_lane = args[2]['start_lane']

        def start_lane_final(self, lane, *, old_start, apps_f, reds_f):
            if lane not in apps_f.keys():
                return old_start(self, lane)

            ideal = apps_f[lane](self)  # subdivision -> input per reapportionment
            return reds_f[lane](self, lane, self.get_lane_sub(lane), ideal)

        args[2]['start_lane'] = partial(start_lane_final, old_start=start_lane, apps_f=apps, reds_f=reds)

        return super().__new__(cls, *args, **kwargs)


class lane_middle(type):
    """
    Un nodo intermedio, propone al nodo superiore, riceve la correzione e corregge i nodi inferiori
    """

    def __new__(cls, *args, lane_middle, **kwargs):
        # Step 1: flip the arguments
        params = dict()
        for l_n, ps in lane_middle.items():
            for k in ps:
                if k not in params:
                    params[k] = dict()
                params[k][l_n] = ps[k]

        # Funzione is_lane_endpoint('lane') (controlla che la funzione non esista già, nel caso decorala e basta)
        def func(self, lane_n):
            return False

        if 'is_lane_endpoint' in args[2]:
            func = args[2]['is_lane_endpoint']

        def is_lane_endpoint(self, tipo, *, old_lane_f):
            return old_lane_f(self, tipo)

        args[2]['is_lane_endpoint'] = partial(is_lane_endpoint, old_lane_f=func)

        # Funzione get_lane_sub('lane') return

        # Funzione proponi('lane', **kwargs)

        # Funzione eleggi('lane', **kwargs)


class lane_bottom(type):
    """
    Il nodo che riceve le informazioni dai punti precedenti ed elegge dei rappresentanti

    Ha la funzione per eleggere, per fornire una proposta e per ricevere il valore corretto
    """

    def __new__(cls, *args, lane_bottom_args, **kwargs):
        def lane_end_old(self, tipo):
            return False

        if 'is_lane_endpoint' in args[2]:
            lane_end_old = args[2]['is_lane_endpoint']

        def is_lane_endpoint(self, tipo, *, old_lane_f, lane_head_p):
            if tipo in lane_head_p.keys():
                return True
            else:
                return old_lane_f(self, tipo)

        args[2]['is_lane_endpoint'] = partial(is_lane_endpoint, old_lane_f=lane_end_old, lane_head_p=lane_bottom)

    # funzione proponi('lane', **kwargs)

    # funzione eleggi('lane', **kwargs)

    # funzione eletti('lane')


class direct_election(type):
    """
    Il numero prioritario può essere fornito ma di default è 0

    Un nodo che è sia lane_head che lane_bottom
    Elegge direttamente i rappresentanti. Salva in hub come punto di partenza

    Deve sapere quanti rappresentanti eleggere, con che criterio
    """

    # funzione eleggi('lane', **kwargs)

    # funzione eletti('lane')

    # funzione is_end_of_lane('lane') true
