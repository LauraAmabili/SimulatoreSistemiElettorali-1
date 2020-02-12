import src.GlobalVars
from src import Commons

commons = Commons


class totFilter(type):
    """
    Le classi con questa meta hanno la funzione filter(self, inst_geo, type_tot, row, df)

    Parametri passati a filter:
        + district_inst, totals_type, row, full_df, sbarramenti

    Un filtro può essere:
    + condizione
    + predicato composto da altri filtri della stessa PolEnt
    + un filtro di un'altra polEnt a cui passo solo district

    Inoltre posso specificare se un filtro è memoizable (il filtro restituisce sempre
    lo stesso valore indipendentemente da come è chiamato

    Infine potrei dover fare un rebase, che vuol dire spostarmi in un livello geografico
    superiore

    Che dati uso?

    Ho a disposizione:
        + Il distretto
        + Il nome della funzione
        + la linea specifica
        + il dataframe completo
        + la lista degli sbarramenti

    1. Se sbarramenti è una lista procedo in ordine, devono essere verificati tutti
    2. Se non è una lista allora procedo

    Lista eletta:
        type: dataframe
        rebase: Nazione
        source:
            totals: Liste
        column: Voti
        criteria: gt
        logic: relative
        target: 0.03

    Coalizione partiti:
        type: filter_map
        criteria: any
        filter: eletto
        targets: Partiti # trova i partiti sottostanti la coalizione

    Coalizione soglia:
        rebase: Nazione
        source:
            totals: Coalizione
        criteria

    Coalizione eletta:
        and:
            - fil1
            - not: fil2
            - or:
                - fil3
                - fil4
    """

    @classmethod
    def parse_tot(mcs, old_filter, *, filters):
        filt_dict = {name: mcs.parse_filter_action(name, **d) for name, d in filters.items()}
        # parse_filter_action restituisce due funnzioni, la prima dice se devo applicare il filtro a questo livello
        # (prende in input district e total)
        # la seconda applica il filtro
        old_filter = lambda *x: None

        def filter(self, district, *, total=None, row=None, dataframe=None, sbarramenti):
            if type(sbarramenti) == list:
                for i in sbarramenti:
                    if not self.filter(district, total=total, row=row, dataframe=dataframe, sbarramenti=i):
                        return False
                return True
            if sbarramenti not in filt_dict:
                return old_filter(self, district, total, row, dataframe, sbarramenti)

            apply_check, filter_f = filt_dict[sbarramenti]
            if apply_check(district=district, total=total):
                return filter_f(self, district, total=total,
                                row=row,
                                dataframe=dataframe,
                                sbarramenti=sbarramenti)
            else:
                return True

        return filter

    @classmethod
    def parse_filter_function_wrapper(mcs, filter_name, *, memoizable=False, rebase=None, **conf):

        act_filt = mcs.parse_filter_function(filter_name, **conf)

        def filter(self, district, **kwargs):
            if memoizable:
                if filter_name in self.memoized:
                    return self.memoized[filter_name]

            if rebase is not None:
                district = src.GlobalVars.Hub.get_superdivision(district, rebase)
                district = src.GlobalVars.Hub.get_instance(rebase, district)
                kwargs.pop('dataframe')

            res = act_filt(self, district, **kwargs)
            if memoizable:
                self.memoized[filter_name] = res

            return res

        return filter

    @classmethod
    def parse_value_filter(mcs, *, source=None, column_key=None, column, criteria, logic='absolute', target):
        """
        source: se None uso il dataframe fornito, si supponga che self sia un distretto geografico
        column_key: solo se uso source, mi dice quale colonna guardare per identificare la linea
        La colonna deve essere la stessa per la row e per il df
        column: la colonna da confrontare
        criteria: gt,lt,eq
        logic: absolute/relative
        """
        def value_filter(self, district, *, row, dataframe=None, **kwargs):
            if source is not None:
                dataframe = source({'self': district})
                row = dataframe[dataframe[column_key] == row[column_key]].iloc[0]

            if logic == 'relative':
                s = dataframe[column].sum()
                c_v = row[column] / s
            else:
                c_v = row[column]

            if criteria == 'gt':
                return c_v > target
            if criteria == 'lt':
                return c_v < target
            else:
                return c_v == target

        return value_filter


    @classmethod
    def parse_membership_filter(mcs, source):
        def member_filt(self, district, **kwargs):
            l = source(locals())
            return (self in l) or (self.name in l)

        return member_filt

    @classmethod
    def parse_delegate_filter(mcs, *, variable, filter):
        """
        Come rebase ma per le polEnt, chiama il filtro sulla PolEnt contenuta in una data variabile della PolEnt corrente
        """

        def filt_del(self, district, **kwargs):
            v = getattr(self, variable)
            if type(v) == str:
                v = src.GlobalVars.Hub.get_instance('PolEnt', v)
            return v.filter(district, **kwargs)

        return filt_del

    @classmethod
    def parse_map_filter(mcs, *, source, type="any", count=None, sbarramento):
        """
        Come delegate ma su una lista

        Type può essere any/all/less/more/exactly

        count indica il valore (intero) per less/more/exactly
        """

        def map_filter(self, district, **kwargs):
            lis = source(locals())
            if type(lis[0]) == str:
                lis = [src.GlobalVars.Hub.get_instance('PolEnt', i) for i in lis]
            if type == "any":
                for i in lis:
                    if i.filter(district, sbarramento=sbarramento):
                        return True
                return False
            if type == "all":
                for i in lis:
                    if not i.filter(district, sbarramento=sbarramento):
                        return False
                return True
            else:
                c = 0
                for i in lis:
                    if i.filter(district, sbarramento=sbarramento):
                        c += 1

                if type == 'less':
                    return c < count
                if type == "more":
                    return c > count
                else:
                    return c == count

        return map_filter

    @classmethod
    def parse_predicate_filter(mcs, **kwargs):
        """
        Costruisce un predicato a partire da filtri

        Le parole chiave possono essere:
        + and
        + or
        + not

        and e or contengono liste di lunghezza arbitraria, not un valore e basta

        gli elementi delle liste (o i valori) possono essere:
            + stringa (chiama filter con riferimento solo al district
        """

        def filter_pred(self, district, *, sbarramento, **kwargs):

            if 'and' in kwargs:
                for i in kwargs['and']:
                    if not self.filter(district, sbarramento=i):
                        return False
                return True
            if 'or' in kwargs:
                for i in kwargs['or']:
                    if self.filter(district, sbarramento=i):
                        return True
                return False
            if 'not' in kwargs:
                return not self.filter(district, sbarramento=kwargs['not'])

        return filter_pred

    @classmethod
    def parse_filter_function(mcs, type, **kwargs):
        if type == "dataframe":
            pass
            # TODO: dataframe e value sono gli stessi, solo uno è relativo al resto della colonna e l'altro è assoluto
        if type == "value":
            pass
        if type == "membership":  # controlla se self o self.name compare in una qualche lista
            pass
        if type == "delegate":  # applica il filtro ad una polent superiore
            pass
        if type == "map":  # applica il filtro ad una lista di polent sottostanti
            pass
        if type == "predicate":  # crea una espressione in logica dei predicati usando filtri di self
            return mcs.parse_predicate_filter(**kwargs)

    @classmethod
    def parse_conf(mcs, conf):
        return conf

    @classmethod
    def parse_filter_action(mcs, name, param):
        return check_filter, apply_filter

