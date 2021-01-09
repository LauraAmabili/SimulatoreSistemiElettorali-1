class ExtendableIterator:
    def __init__(self, set_start):
        self.s = set(set_start)

    def add_el(self, el):
        self.s.add(el)

    def __next__(self):
        try:
            return self.s.pop()
        except KeyError:
            raise StopIteration

    def __iter__(self):
        return self


class ActHub:
    def __init__(self, *args):
        self.instances_dict = {}  # Class_name: {Inst_name: instance}
        self.subs_relations = {}  # Class_name:
        self.subclasses = {}
        self.lanes = {}
        self.pol = {}
        self.lane_tails = {}
        self.elected = {}  # nome_cand : informazioni
        self.electors = []
        self.assigned_seats = {}

    def run_exec(self):

        # ordina le lanes secondo 'order_number'
        # quindi order_number è la priorità, viene
        # eseguita prima la lane con order_numer piu basso
        orders = sorted(self.lanes.keys())
        for i in orders:

            ret = []
            exec_return = []

            for l_n, h_c in self.lanes[i]:

                instances = self.get_instances(h_c)
                instances = [self.get_instance(h_c, n_i) for n_i in instances]

                ret.extend([instruction for inst in instances for instruction in inst.exec_lane(l_n)])

            polEnt_list = self.subclasses.get('PolEnt')
            if 'Candidato' in polEnt_list :

                prop_nomi = set()
                for district, name_lista, elector, seats in ret:
                    self.electors.append((district, name_lista, elector, seats))
                    p = self.get_instance("PolEnt", elector)
                    for name in p.elect(name_lista, district, seats):
                        prop_nomi.add(name)
                iter_nomi = ExtendableIterator(prop_nomi)

                
                for i in iter_nomi:

                    c = self.get_instance("PolEnt", i)
                    info, next = c.pick()
                    for nome_next in next:
                        iter_nomi.add_el(nome_next)
                    self.elected[i] = info
                exec_return = [self.electors, self.elected]
            else: 
                exec_return = ret
                
        return exec_return

    def get_elected(self, lane=None, polEnt=None):
        """

        """


    def add_lane_tail(self, lane_name, class_name):
        self.lane_tails[lane_name] = class_name

    def get_political_subs(self, sup, sub_type, *, strict=False, actual=False):
        """
        sup è un'istanza
        sub_type è un nome di classe
        """
        if actual:
            l = self.get_political_subs(sup, sub_type, strict=strict, actual=False)
            return [self.get_instance("PolEnt", i) for i in l]

        if strict:
            return self.pol.get(sup.name, {}).get(sub_type, {})

        synonims = self.subclasses.get(sub_type, [])
        synonims.append(sub_type)

        return {el for typ in synonims for el in self.get_political_subs(sup,
                                                                         typ,
                                                                         strict=True,
                                                                         actual=actual)}

    def add_political_sub(self, sub, sup, typ):
        o_sup = self.pol.get(sup, {})

        o_sup_class = o_sup.get(typ, set())
        o_sup_class.add(sub)

        o_sup[typ] = o_sup_class

        self.pol[sup] = o_sup

    def get_path(self, sup_t, sub_t):
        if sub_t in self.subs_relations[sup_t]:
            return [sub_t]

        for i in self.subs_relations[sup_t].keys():
            v = self.get_path(i, sub_t)
            if v != []:
                return [i] + v
        return []

    def get_subdivisions(self, sup, sub_class, instance=False):
        #print("Get sub")
        typ = None
        inst = sup
        if type(sup) == tuple:
            typ = sup[0]
            inst = self.get_instance(typ, sup[1])
        else:
            typ = sup.type
            name = sup.name

        path = self.get_path(typ, sub_class)
        ents = [inst]
        for i in path[:-1]:
            ents = [j for en in ents for j in self.get_subdivisions_direct(en, i, True)]

        return [j for en in ents for j in self.get_subdivisions_direct(en, sub_class, instance)]

    def get_subdivisions_direct(self, sup, sub_class, instance):
        typ = None
        inst = sup
        if type(sup) == tuple:
            typ = sup[0]
            inst = self.get_instance(typ, sup[1])
        else:
            typ = sup.type
            name = sup.name

        var_name = self.subs_relations[typ][sub_class]

        lis = getattr(inst, var_name)
        if instance:
            return list(map(lambda n: self.get_instance(sub_class, n), lis))
        else:
            return lis

    def get_subdivisions_old(self, sup, sub_name, instance=False):
        """
        sup: o un'istanza di una geoEnt, o una tupla (nomeClasse, nomeIstanza)
        sub_name: nome classe target

        return: list of names (stringhe)
        """
        typ = None
        inst = sup
        if type(sup) == tuple:
            typ = sup[0]
            inst = self.get_instance(typ, sup[1])
        else:
            typ = sup.type
            name = sup.name

        var_name = self.subs_relations[typ][sub_name]

        lis = getattr(inst, var_name)
        if instance:
            return list(map(lambda n: self.get_instance(sub_name, n), lis))
        else:
            return lis

    def register_subclass(self, subclass, superclass):
        ex = self.subclasses.get(superclass, [])
        ex.append(subclass)
        self.subclasses[superclass] = ex

    def get_instances(self, classe, strict=False):
        #print("Get instances: ", classe, strict)
        """
        Ricava tutte le istanze di tutte le sottoclassi di classe, se necessario 
        """
        if strict:
            return self.instances_dict.get(classe, [])

        subs = self.subclasses.get(classe, [])
        subs = [classe] + subs

        return [el for i in subs for el in self.instances_dict.get(i, [])]

    def get_superdivision(self, sub, sup_name):
        """
        sub: o un'istanza o una tuple
        sup_name: nome classe target

        return nome istanza target
        """
        tops = self.get_instances(sup_name)
        typ = None
        inst = sub
        if type(sub) == tuple:
            typ = sub[0]
            name = sub[1]
            inst = self.get_instance(typ, sub[1])
        else:
            typ = sub.type
            name = sub.name

        for i in tops:
            if name in self.get_subdivisions((sup_name, i), typ):
                return i
        raise KeyError("No such superdivision")

    def add_instance(self, class_name, inst_name, instance):
        instances = self.instances_dict.get(class_name, {})
        instances[inst_name] = instance
        self.instances_dict[class_name] = instances

    def get_instance(self, class_name, inst_name):

        #print("Getting instance", class_name, inst_name)
        subs = self.subclasses.get(class_name, [])

        for i in subs:
            if inst_name in self.get_instances(i):
                return self.instances_dict[i][inst_name]

        
        return self.instances_dict[class_name][inst_name]

    def add_subdiv(self, sup_type, sub_type, var_name):
        """
        Records that instances of sup_type have instances of sub_type
        stored in self.var_name
        """
        sup_dict = self.subs_relations.get(sup_type, {})
        sup_dict[sub_type] = var_name
        self.subs_relations[sup_type] = sup_dict

    def register_lane(self, name, head_class, order):
        # self.lanes è il dizionario che contiene tutte le lane create
        # prende la lane con order passato,
        # se non c'è di default restituisce lista vuota []
        exist = self.lanes.get(order, [])

        # appende il nome della lane e il nome della classe della lane
        exist.append((name, head_class))

        # aggiunge i valori al dizionario delle lane
        self.lanes[order] = exist


Hub = ActHub()
