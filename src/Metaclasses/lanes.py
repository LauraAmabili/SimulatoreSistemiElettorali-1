# -*- coding: utf-8 -*-
import pandas as pd
import src.GlobalVars
import src.utils
import src.Commons
from src import Commons

commons = Commons

class lanes(type):
    def __new__(mcs, *args, lane=None, lanes_propose=None, **kwargs):
        if lane is None:
            lane = {}

        if lanes_propose is None:
            lanes_propose = {}

        list_lanes = [i for i in lane.items()]
        fun_lanes = {n: mcs.parse_lane_fun(n, **kws, class_name=args[0]) for n, kws in list_lanes}
        # fun lanes è un dizionario di funzioni che accettano:
        # + self
        # + lane
        # + *information (solo node e tail)
        # + distribution (kwarg) (solo node e tail)

        o_lanes = args[2].get('exec_lane', lambda *a, **k: None)

        def new_exec(self, name, *args, **kwargs):
            """
            args sono le informazioni
            kwargs contiene solo (opzionalmente) la distribuzione
            """
            if name not in fun_lanes:
                return o_lanes(self, name, *args, **kwargs)
            return fun_lanes[name](self, name, *args, **kwargs)

        args[2]['exec_lane'] = new_exec
        args[2]['propose'] = mcs.parse_propose(lanes_propose, args[2].get('propose', lambda *a, **kw: None))

        return super().__new__(mcs, *args, **kwargs)

    @staticmethod
    def parse_conf(conf):
        return conf

    @classmethod
    def parse_operation_lane(mcs, sub_level, *,
                             collect_type, ideal_distribution, corrector, collect_constraints=None,
                             forward_distribution=False, **kwargs):
        """
        sub_level: Il livello inferiore della lane
        collect_type: il tipo di propose che sarà chiamato sui livelli inferiori
        ideal_distribution:
            + '$': La distribuzione precedente
            + str: Il tipo di propose da chiamare
            + dict: dict['source'] è la funzione da chiamare
        corrector: la funzione da chiamare per avere la correzione
        collect_constraints:
            + None
            + '$': la distribuzione precedente
            + str: il tipo di propose da chiamare su self
        forward_distribution: se True allora rende irrilevanti le operazioni sulla distribuzione

        Genera la funzione di una singola operazione, accetta:
            + locs
            + prev_distribution
            + info_specific
            + info_general

        Restituisce:
            + distribution
            + new_general_info
            + new_specific_info
        """
        ideal_distr = ideal_distribution
        corrector = eval(corrector)

        def operation_fun(loc, specific_info, info_district, *general_info, distribution):
            """
            loc: Il namespace locale
            specific_info: le informazioni specifiche preesistenti (un dizionario per ogni sottolivello)
            info_district: informazioni preesistenti per il livello corrente, possono essere modificate
            general_info: una lista di informazioni generiche, non modificare
            distribution: un dataframe con due colonne [Elettore, Seggi] (o equivalenti)
            """

            district = eval("self", globals(), loc)

            subs = src.GlobalVars.Hub.get_subdivisions(district, sub_level)
            gen_info_new = {}

            if type(ideal_distr) != str:
                # print("Locals prima di chiamare abcd: ", loc)
                ideal_distrib_dynamic = ideal_distr['source'](loc, district)
            elif ideal_distr == "$":
                ideal_distrib_dynamic = distribution
            else:
                ideal_distrib_dynamic, gen_info_new = \
                    district.propose(ideal_distr, *general_info, distribution=distribution)

            for k, v in gen_info_new.items():
                d = info_district.get(k, {})
                d.update(v)
                info_district[k] = d
            #
            # TODO: il meccanismo con cui passo le informazioni generali è un disastro
            #
            general_info_lower_lvl = [info_district] + list(general_info)

            def get_proposal(name, *gen_info):
                s = src.GlobalVars.Hub.get_instance(sub_level, name)
                if collect_constraints is None:
                    distr, loc_info_new = s.propose(collect_type, {}, *general_info_lower_lvl, distribution=ideal_distrib_dynamic)
                elif collect_constraints == '$':
                    constr = distribution.get(name, pd.DataFrame())
                    distr, loc_info_new = s.propose(collect_type, {}, *general_info_lower_lvl,
                                                    constraint=constr,
                                                    distribution=ideal_distrib_dynamic)
                else:
                    constr = district.propose(collect_constraints, *general_info_lower_lvl, distribution=ideal_distrib_dynamic)
                    distr, loc_info_new = s.propose(collect_type, {}, *general_info_lower_lvl,
                                                    constraint=constr,
                                                    distribution=ideal_distrib_dynamic)

                return distr, loc_info_new
            # FIXME: AGGIUSTARE TUTTO QUI
            #        PASSO LOCAL, DISTRIC, GENERAL RICEVO NEW LOCAL DA PROPOSE, NEW LOC E NEW DISTRICT DA CORRECT
            o_distr = distribution
            distribution = {}
            new_general = {}
            new_specific = {}
            # print("line 147, subs= ", subs)
            for i in subs:
                n_dist, n_spec = get_proposal(i, *general_info)
                distribution[i] = n_dist
                new_specific[i] = n_spec

            specific_cumulative = {k: v for k, v in specific_info.items()}
            for k, v in new_specific.items():
                d_t = specific_cumulative.get(k, {})
                d_t.update(v)
                specific_cumulative[k] = d_t

            correct_distr, new_loc,  new_gen = corrector(district, ideal_distrib_dynamic,
                                                        distribution,
                                                        specific_cumulative, *general_info_lower_lvl)

            for k, v in info_district.items():
                d = new_gen.get(k, {})
                d.update(v)
                new_gen[k] = d

            specific_new_cumulated = {k: v for k, v in new_specific.items()}
            for k, v in new_loc.items():
                d_t = specific_new_cumulated.get(k, {})
                d_t.update(v)
                specific_new_cumulated[k] = d_t

            if forward_distribution:
                # print("Forwarding")
                return o_distr, specific_new_cumulated, new_gen
            else:
                # print("Modified distr")
                return correct_distr, specific_new_cumulated, new_gen
        return operation_fun

    @classmethod
    def parse_ops_lane(mcs, sub_level, *operations):
        """
        sub_level: Il livello inferiore
        operations: una lista di operazioni

        Genera una funzione che accetta una distribuzione, le informazioni e restituisce nuove informazioni e una nuova
        distribuzione

        Restituisce:
            distribution
            generic_info_new
            specific_info_new
        """
        ops_funcs = list(map(lambda o_d: mcs.parse_operation_lane(sub_level, **o_d), operations))
        # ognuna di queste funzioni accetta:
        # + loc, variabili locali
        # + specific info: dizionario di informazioni specifiche
        # + *general_info: lista informazioni comuni TODO: fare in modo che il primo componente sia modificabile
        # + distribution (kw): la distribuzione precedente
        #
        # e restituisce:
        # + nuova distribuzione
        # + nuove informazioni specifiche
        # + nuove informazioni comuni (o informazioni comuni complete?) TODO: far rispettare queste condizioni

        def generated_operations(loc, district_gen_info, *general_info, distribution):
            """
            loc: il namespace locale
            distribution: il dataframe [Elettore, Seggi]
            district_gen_info: le informazioni generiche del distretto
            general_info: una lista di informazioni comuni

            Restituisce:

            distribution: nuova distribuzione
            spec_info: Un dizionario su nuove informazioni specifiche ai sottolivelli
            district_gen_info: Le informazioni comuni a questo distretto
            """
            spec_info = {}
            for f in ops_funcs:
                #print("Info generic: ", district_gen_info)
                #print("Info specific: ", spec_info)
                #print("-------------")
                n_distr, sp_new_cum, new_generic = f(loc, spec_info,
                                                     district_gen_info, *general_info,
                                                     distribution=distribution)
                distribution = n_distr

                specific_cumulative = {k: v for k, v in spec_info.items()}
                for k, v in sp_new_cum.items():
                    d_t = specific_cumulative.get(k, {})
                    d_t.update(v)
                    specific_cumulative[k] = d_t
                spec_info = specific_cumulative

                gen_cumulative = {k: v for k, v in district_gen_info.items()}
                for k, v in new_generic.items():
                    d_t = gen_cumulative.get(k, {})
                    d_t.update(v)
                    gen_cumulative[k] = d_t
                district_gen_info = gen_cumulative
            return distribution, spec_info, district_gen_info
        return generated_operations

    @classmethod
    def parse_lane_tail(mcs, lane_name, *, info_name, class_name, **kwargs):
        """
        lane_name: Il nome della lane
        info_name: Il nome da dare al nome del distretto nelle informazioni

        Genera la funzione che riceve una distribuzione come kwarg, registra le informazioni e distribuisce seggi
        """
        src.GlobalVars.Hub.add_lane_tail(lane_name, class_name)

        def exec_lane_tail(self, lane, *info, distribution):
            """
            lane: nome della lane
            info: lista di informazioni relative al distretto
            distribution: dataframe
            """

            info_cumulative = {}
            for dic in info[-1::-1]:
                for k, inf in dic.items():
                    d_t = info_cumulative.get(k, {})
                    d_t.update(inf)
                    info_cumulative[k] = d_t
            for k in info_cumulative:
                info_cumulative[k][info_name] = self.name
                t = src.GlobalVars.Hub.get_instance("PolEnt", k)
                t.log(self, lane_name, **info_cumulative[k])

            ret = []
            for _, r in distribution.iterrows():
                ret.append((self, lane_name, r.iloc[0], int(r.iloc[1])))
            return ret
        return exec_lane_tail

    @classmethod
    def parse_lane_node(mcs, lane_name, *, operations, info_name, sub_level, **kwargs):
        """
        lane_name: Il nome della lane
        operations: Le operazioni da aggiungere
        info_name: Il nome da dare al nome del distretto nelle informazioni
        sub_level: il livello inferiore

        Genera la funzione che prende una distribution come kwarg, la processa e inoltra a livelli inferiori
        """
        ops_f = mcs.parse_ops_lane(sub_level, *operations)
        # Ops f accetta:
        # + loc
        # + distribution
        # + district_gen_info
        # + *general_info
        # e restituisce:
        # + distribution
        # + spec_info
        # + district_gen_info

        def exec_lane_node(self, lane, district_info, *info, distribution): # il info[0] è locale, quindi modificabile
            """
            lane:
            info:
            distribution:
            """
            distr, spec_info, gen_info = ops_f({'self':self, 'commons':Commons, 'Commons':Commons}, district_info, *info, distribution=distribution) #
            subs = src.GlobalVars.Hub.get_subdivisions(self, sub_level)

            distr_info = {k: v for k, v in district_info.items()}
            for k, v in gen_info.items():
                d = distr_info.get(k, {})
                d.update(v)
                d[info_name] = self.name
                distr_info[k] = d

            info = [distr_info] + list(info)

            rets = []
            sub_info = {k: v for k, v in
                        spec_info.items()}  # TODO: distinguere gen_info e loc_info, gen info riguarda il livello superiore
                                            #       loc_info riguarda il livello che chiamo
            for sub, sub_inf in sub_info.items():
                for k, v in sub_inf.items():
                    v[info_name] = self.name

            for i in subs:
                inst = src.GlobalVars.Hub.get_instance(sub_level, i)
                rets.extend(inst.exec_lane(lane_name, sub_info.get(i,{}), *info, distribution=distr[i]))
            return rets
        return exec_lane_node

    @classmethod
    def parse_lane_head(mcs, lane_name, *, first_input, order_number, class_name, **kwargs):
        """
        lane_name:
        first_input: il nome della propose da usare per primo input
        order_number: Il numero di priorità, lane con numeri minori vengono eseguite prima di lane con numeri maggiori
        class_name: il nome della classe

        La head, usa distribution per generare una distribuzione ideale e poi la modifica con le operazioni
        """
        src.GlobalVars.Hub.register_lane(name=lane_name, head_class=class_name, order=order_number)
        f = mcs.parse_lane_node(lane_name, **kwargs)

        def exec_head(self, lane):
            distribution, info = self.propose(first_input)
            return f(self, lane_name, info, distribution=distribution)
        return exec_head
    @classmethod
    def parse_lane_only(mcs, lane_name, *, distribution, order_number, class_name, **kwargs):
        """
        lane_name:
        distribution: il nome della propose da usare
        order_number:
        class_name:

        Genera la funzione che fa' tutto in una lane single-step
        """

        src.GlobalVars.Hub.register_lane(name=lane_name, head_class=class_name, order=order_number)

        distr_name = distribution
        f = mcs.parse_lane_tail(lane_name, class_name=class_name, **kwargs)

        def exec_only(self, lane):
            distrib, info = self.propose(distr_name)

            return f(self, lane_name, *info, distribution=distrib)

        return exec_only

    @classmethod
    def parse_lane_fun(mcs, lane_name, *, node_type, **kwargs):
        #print("Test")
        """
        Returns the function which is to be called when exec_lane(lane_name, *info, **kwargs)
         is called
        """
        if node_type == "only":
            return mcs.parse_lane_only(lane_name, **kwargs)
        if node_type == "head":
            return mcs.parse_lane_head(lane_name, **kwargs)
        if node_type == "tail":
            return mcs.parse_lane_tail(lane_name, **kwargs)
        if node_type == "node":
            return mcs.parse_lane_node(lane_name, **kwargs)

    @classmethod
    def parse_propose_distribution_dict(mcs, key, seats, selector, **kwargs):
        """
        key: la chiave, una stringa
        seats:
            + Un intero
            + Una stringa (il valore di una colonna)
        selector: filtra le linee, di due tipi
            + Ordina le linee in base ad una colonna e restituisce le prime n
            + Per ogni linea controlla che il valore in una colonna rispetti un criterio
        """

        if 'take' in selector:
            fun_distr = src.utils.parse_row_selector_take(**selector)
        else:
            fun_distr = src.utils.parse_row_selector_value(**selector)

        def distribution_derive(source_df):
            """
            source_df: dataframe
            """
            filtered = fun_distr(source_df)
            df = filtered[[key]]
            if type(seats) == int:
                df['Seats'] = seats
            elif type(seats) == str:
                df['Seats'] = filtered[seats]

            return df

        return key, distribution_derive # distribution_derive è una funzione

    @classmethod
    def parse_propose_function(mcs, source, distribution, info, info_key=None, **kwargs):
        """
        source: la funzione di partenza
        distribution: come derivare la distribuzione, può essere una lista di due colonne
                      o un dizionario che specifica che colonne prendere e quali righe prendere
        info: quali colonne mettere come informazioni
        info_key: se la chiave delle info è diversa dalla chiave della distribuzione
        """

        def distribution_list(df):
            return df[distribution]

        if type(distribution) == list:
            distr_fun = distribution_list
            key_d = distribution[0]
        else:
            key_d, distr_fun = mcs.parse_propose_distribution_dict(**distribution)
            # distr_fun accetta un dataframe

        if info_key is None:
            info_key = key_d


        def return_function_propose(self, kind, *information, constraint=None, distribution=None, **kwargs):
            """
            kind: il tipo della propose
            information: informazioni applicabili al livello

            Restituisce:
            distribution: dataframe
            info_dict: Dict[str, Dict[str, obj]]
            """
            #TODO: aggiustare cosa prende la propose, idealmente tra i parametri  ... VEDI AUDIO TELEGRAM
            locs = locals()
            data = source(locs, information=information, constraint=constraint, distribution=distribution)

            info_dict = {}

            for _, s in data.iterrows():
                info_dict[s[info_key]] = {k: s[k] for k in info}
            distr_ret = distr_fun(data)
            distr_ret = distr_ret[distr_ret.iloc[:, 1] > 0].copy()
            return distr_fun(data), info_dict

        return return_function_propose

    @classmethod
    def parse_propose(mcs, configuration, old_f):
        """
        Receives the propose dict, returns the propose function
        """

        fun_list = map(lambda x: (x[0], mcs.parse_propose_function(**x[1])), configuration.items())

        fun_map = {n: f for n, f in fun_list}

        def propose(self, name, *args, **kwargs):
            #print("Fun_map: ", fun_map)
            if name not in fun_map:
                # print("Old_list")
                return old_f(self, name, *args, **kwargs)
            return fun_map[name](self, name, *args, **kwargs)

        return propose
