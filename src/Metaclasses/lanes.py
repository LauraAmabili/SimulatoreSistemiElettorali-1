# -*- coding: utf-8 -*-
import pandas as pd
import src.GlobalVars
import src.utils


class lanes(type):
    def __new__(mcs, *args, **kwargs):
        pass

    @staticmethod
    def forward_info_gen_distr(tail, lane_name, distribution, *info):
        """
        La funzione chiamata da lane_tail e lane_only passando self, distribuzione, nome della lane, le info
        Inoltra le info e genera la lista che lane_exec deve restituire
        """
        info_final = dict()
        for i in info[-1::-1]:
            for target, info_targ in i.items():
                info_targ_total = info_final.get(target, dict())
                info_targ_total.update(info_targ)
                info_final[target] = info_targ_total

        for el, info in info_final.items():
            t = src.GlobalVars.Hub.get_instance("PolEnt", el)
            s = pd.Series(info)
            t.log(tail, lane_name, s)

        proposals = []
        for r in distribution.iterrows():
            proposals.append((tail, lane_name, r.iloc[0], r.iloc[1]))

        return proposals

    @classmethod
    def parse_operation_lane(mcs, sub_level, *,
                             collect_type, ideal_distribution, corrector, collect_constraints=None, **kwargs):
        """
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

        def operation_fun(loc, specific_info, *general_info, distribution):

            district = eval("self", globals(), loc)

            subs = src.GlobalVars.Hub.get_subdivisions(district, sub_level)

            def get_proposal(name):
                s = src.GlobalVars.Hub.get_instance(sub_level, name)
                if collect_constraints is None:
                    distr, loc_info_new = s.propose(collect_type)
                elif collect_constraints == '$':
                    constr = distribution.get(name, pd.DataFrame())
                    distr, loc_info_new = s.propose(collect_type, constr)
                else:
                    constr = district.propose(collect_constraints)
                    distr, loc_info_new = s.propose(collect_type, constr)

                return distr, loc_info_new

            distributions = {}
            new_general = {}
            new_specific = {}
            print("line 75, subs= ", subs)
            for i in subs:
                n_dist, n_spec = get_proposal(i)
                distributions[i] = n_dist
                new_specific[i] = n_spec

            if type(ideal_distr) != str:
                ideal_distribution = ideal_distr['source'](loc, district)
            if ideal_distr == "$":
                ideal_distribution = distribution
            else:
                ideal_distribution = district.propose(ideal_distr)

            specific_cumulative = {k: v for k, v in specific_info.items()}
            for k, v in new_specific.items():
                d_t = specific_cumulative.get(k, {})
                d_t.update(v)
                specific_cumulative[k] = d_t

            correct_distr, new_loc, new_gen = corrector(district, ideal_distribution,
                                                        distributions,
                                                        specific_cumulative, *general_info)

            specific_new_cumulated = {k: v for k, v in new_specific.items()}
            for k, v in new_loc.items():
                d_t = specific_new_cumulated.get(k, {})
                d_t.update(v)
                specific_new_cumulated[k] = d_t

            return correct_distr, specific_new_cumulated, new_gen
        return operation_fun

    @classmethod
    def parse_ops_lane(mcs, sub_level, *operazioni):
        """
        Genera una funzione che accetta una distribuzione, le informazioni e restituisce nuove informazioni e una nuova
        distribuzione

        Restituisce:
            distribution
            generic_info_new
            specific_info_new
        """
        ops_funcs = list(map(lambda o_d: mcs.parse_operation_lane(sub_level, **o_d), operazioni))

        def generated_operations(loc, distribution, district_gen_info, *general_info):
            spec_info = {}
            for f in ops_funcs:
                print("Info generic: ", district_gen_info)
                print("Info specific: ", spec_info)
                print("-------------")
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
    def parse_lane_tail(mcs, lane_name, *, info_name, **kwargs):
        """
        Genera la funzione che riceve una distribuzione come kwarg, registra le informazioni e distribuisce seggi
        """
        def exec_lane_tail(self, lane, *info, distribution):
            info_cumulative = {}
            for dic in info[-1::-1]:
                for k, inf in dic.items():
                    d_t = info_cumulative.get(k, {})
                    d_t.update(inf)
                    info_cumulative[k] = d_t
            for k in info_cumulative:
                info_cumulative[k][info_name] = self.name
                t = src.GlobalVars.Hub.get_instance("PolEnt", k)
                t.log(self, lane_name, info_cumulative[k])

            ret = []
            for r in distribution.iterrows():
                ret.append((self, lane_name, r.iloc[0], int(r.iloc[1])))
            return ret
        return exec_lane_tail

    @classmethod
    def parse_lane_node(mcs, lane_name, *, operations, info_name, sub_level, **kwargs):
        """
        Genera la funzione che prende una distribution come kwarg, la processa e inoltra a livelli inferiori
        """
        ops_f = mcs.parse_ops_lane(sub_level, *operations)

        def exec_lane_node(self, lane, *info, distribution):
            distr, spec_info, gen_info = ops_f(locals(), distribution, *info)
            subs = src.GlobalVars.Hub.get_subdivisions(self, sub_level)

            rets = []
            for i in subs:
                sub_info = {k: v for k, v in gen_info.items()}
                for k, v in spec_info.get(i, {}):
                    s = sub_info.get(k, {})
                    s.update(v)
                    s[info_name] = self.name
                    sub_info[k] = s
                inst = src.GlobalVars.Hub.get_instance(sub_level, i)
                rets.extend(inst.exec_lane(lane_name, sub_info, *info, distribution=distr[i]))
        return exec_lane_node

    @classmethod
    def parse_lane_head(mcs, lane_name, *, first_input, **kwargs):
        """
        La head, usa distribution per generare una distribuzione ideale e poi la modifica con le operazioni
        """
        f = mcs.parse_lane_node(lane_name, **kwargs)

        def exec_head(self, lane):
            distribution, info = self.propose(first_input)
            return f(self, lane_name, info, distribution=distribution)


    @classmethod
    def parse_lane_only(mcs, lane_name, *, distribution, **kwargs):
        """
        Genera la funzione che fa' tutto in una lane single-step
        """

        distr_name = distribution
        f = mcs.parse_lane_tail(lane_name, **kwargs)

        def exec_only(self, lane):
            distrib, info = self.propose(distr_name)

            return f(self, lane_name, *info, distribution=distrib)

        return exec_only

    @classmethod
    def parse_lane_fun(mcs, lane_name, *, node_type, **kwargs):
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
        Key: la chiave, una stringa
        seats:
            + Un intero
            + Una stringa (il valore di una colonna)

        selector: filtra le linee, di due tipi
            + Ordina le linee in base ad una colonna e restituisce le prime n
            + Per ogni linea controlla che il valore in una colonna rispetti un criterio
        """

        def distribution_derive(locs, source_df):
            return source_df

        return key, distribution_derive

    @classmethod
    def parse_propose_function(mcs, source, distribution, info, info_key=None, **kwargs):
        """
        source: la funzione di partenza
        distribution: come derivare la distribuzione, può essere una lista di due colonn
                      o un dizionario che specifica che colonne prendere e quali righe prendere
        info: quali colonne mettere come informazioni
        info_key: se la chiave delle info è diversa dalla chiave della distribuzione
        """

        def return_function_propose(locs, *args, **kwargs):
            data = source(locs, )
            return distr, general_information, specific_information

        return return_function_propose

    @classmethod
    def parse_distribution_dict(mcs, key, seats, selector):
        """
        Quando distribution è un dict usa questa funzione

        Key: la chiave
        Seats:
           + Intero
           + Source: funzione che restituisce un intero
           + Stringa che indica una colonna
        Selector: (usa src.utils.selectors)
        """

        def return_distribution_fun(locs, data):
            return distribution

        return key, return_distribution_fun

    @classmethod
    def parse_propose(mcs, configuration):
        """
        Receives the propose dict, returns the propose function
        """
