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
        # formato mcs : class ---> nel caso con i dati europei è 'src.comb_Circoscrizione'

        # formato lane_name : string ---> nel caso con i dati europei è 'Lista'

        # formato info_name : string ---> nel caso con i dati europei è 'Circoscrizione'

        # formato class_name : string ---> nel caso con i dati europei è 'Circosrizione'

        # PROBABILMENTE questa riga aggiunge nelle variabili globali
        # una lane in coda con il nome lane_ name e del tipo class_name
        # ---> nel caso con i dati europei è una lane Circoscrizione di nome Circoscrizione

        src.GlobalVars.Hub.add_lane_tail(lane_name, class_name)

        # questa con i dati europeri viene chiamata 5 volte perchè ci sono
       # 5 Circoscrizioni, infatti CREDO che la Circoscrizione sia il livello piu basso
       #
       # FORSE la lane_tail è la lista
       # 
       # viene eseguita una volta per Circoscrizione
       # essendo chiama dalla terz'ultima riga di parse_lane_node 

        def exec_lane_tail(self, lane, *info, distribution):
            """
            lane: nome della lane
            info: lista di informazioni relative al distretto
            distribution: dataframe
            """

            # formato lane : string ---> nel caso dei dati europei è 'lista'

            # formato info, dizionario :
            #                   - chiave : 'nome_partito'
            #                   - valore : dict{ 'Resto' : float_valore_resto, 'Nazione' : string_nome_nazione }
            #                   oppure
            #                   - chiave : 'nome_candidato'
            #                   - valore : dict{ 'Voti' : int_numero_voti, 'Nazione' : string_nome_nazione }
            #
            # questo formato lo troviamo in exec_lane_node, è lo stesso di sub_info

            # formato distribution : lista di distribuzione dei seggi
            #           esempio Circoscrizione 'V : ITALIA INSULARE'
            #                               Indice  Lista                       Seggi
            #                               0       LEGA SALVINI PREMIER        2
            #                               1       PARTITO DEMOCRATICO         1
            #                               2       FRATELLI D'ITALIA           1
            #                               3       FORZA ITALIA                1
            #                               4       MOVIMENTO 5 STELLE          2

            info_cumulative = {}

            # questo blocco d'istruzioni prende il numero dei voti dati ad ogni singolo
            # candidato e le mette in info_cumulative   

            for dic in info[-1::-1]:
                for k, inf in dic.items():
                    d_t = info_cumulative.get(k, {})
                    d_t.update(inf)
                    info_cumulative[k] = d_t

             # formato info_cumulative, dizionario :
            #                   - chiave : 'nome_partito'
            #                   - valore : dict{    'Voti' : int_numero_totale_voti_parito,
            #                                       'Resto' : float_valore_resto,
            #                                       'Nazione' : string_nome_nazione }
            #                   oppure
            #                   - chiave : 'nome_candidato'
            #                   - valore : dict{ 'Voti' : int_numero_voti, 'Nazione' : string_nome_nazione }
            #
            # questo formato lo troviamo in info, ma viene aggiunto il campo 'Voti' al dizionario del partito


            # questo blocco d'istruzioni aggiunge il campo 'Circoscrizione' al dizionario dei candidati
            # e CREDO loggi il nome della lane e le info di ogni candidato
            for k in info_cumulative:
                info_cumulative[k][info_name] = self.name
                t = src.GlobalVars.Hub.get_instance("PolEnt", k)
                t.log(self, lane_name, **info_cumulative[k])

            # formato info_cumulative, dizionario :
            #                   - chiave : 'nome_partito'
            #                   - valore : dict{    'Voti' : int_numero_totale_voti_parito,
            #                                       'Resto' : float_valore_resto,
            #                                       'Nazione' : string_nome_nazione }
            #                   oppure
            #                   - chiave : 'nome_candidato'
            #                   - valore : dict{    'Voti' : int_numero_voti, 
            #                                       'Nazione' : string_nome_nazione,
            #                                       'Circoscrizione' : string_nome_circoscrizione }
            

            ret = []
            for _, r in distribution.iterrows():
                # r.iloc[0] è il nome del partito
                # r.iloc[1] è il numero di seggi assegnati al partito
                
                # questa riga crea i dati finali dei seggi
                # vedi formato nella prima parte di file OUTPUT (in sublime)
                ret.append((self, lane_name, r.iloc[0], int(r.iloc[1])))
            
             # formato ret, lista :
            #            - formato elementi : (istanza_Circoscrizione, nome_lane_tail, nome_partito, int_numero_seggi_partito)
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

         # formato mcs : classe ---> con i dati europei è src.comb_Nazione

        # formato sub_level : stringa ---> con i dati europei è 'Circoscrizione'

        # formato info_name : stringa ---> con i dati europei è 'Nazione'

        # formato operations, lista :
        #                       - elementi sono dizionari
        # [
        # {'collect_type': 'liste',         'ideal_distribution': '$',  'corrector': 'Commons.correct_europee'                              },
        # {'collect_type': 'candidati',     'ideal_distribution': '$',  'corrector': 'Commons.no_op',       'forward_distribution': True    }
        # ]

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

            # formato district_info, dizionario :
            #   - chiave : nome_partito
            #   - valore : dict{ 'Voti' : int_voti }

            # formato lane : 'lista'

            # formato info : ()

            # formato distribution (NON BEN CAPITO) :
            #               Partito                     Seggi
            #       8       LEGA SALVINI PREMIER        30
            #       12      PARTITO DEMOCRATICO         20


            distr, spec_info, gen_info = ops_f({'self':self, 'commons':Commons, 'Commons':Commons}, district_info, *info, distribution=distribution) #

            # formato distr, dizionario :
            #                   - chiave : 'nome_circoscrizione' --> lo trovi in ExampleDelivery/Instances/Nazione.yaml
            #                   - valore : lista pariti con numero seggi in questo formato :
            #                                                                       'indice'    'nome_partito'  'int_seggi'

            # formato spec_info, dizionario :
            #                   - chiave : 'nome_circoscrizione' --> lo trovi in ExampleDelivery/Instances/Nazione.yaml
            #                   - valore : dizionario :
            #                                   - chiave : 'nome_partito'
            #                                   - valore : dict{ 'Resto' : float_valore_resto }
            #                                   oppure
            #                                   - chiave : 'nome_candidato'
            #                                   - valore : dict{ 'Voti' : int_numero_voti }

            # formato gen_info, dizionario :
            #                       - chiave : 'nome_parito'
            #                       - valore : dict{ 'Voti' : int_ numero_voti } 

            subs = src.GlobalVars.Hub.get_subdivisions(self, sub_level)

            # formato subs : lista contenente i nomi delle suddivisioni dei livelli sottostanti
            #                   in questo caso noi abbiamo che sub_level = 'Circoscrizioni'
            #                   quindi ci viene restituito i nomi delle circoscrizioni in ExampleDelivery/Instances/Nazione.yaml
            #
            #                   il fatto che il sub_level sia 'Circoscrizioni', secondo me, è dato dal file
            #                   ExampleDelivery/Instances/Nazione.yaml riga 11


            # questa istruzione semplicemente copia district_info in distr_info
            distr_info = {k: v for k, v in district_info.items()}
            for k, v in gen_info.items():
                d = distr_info.get(k, {})
                d.update(v)
                # da questa istruzione aggiunge il campo info_name = 'Nazione'
                # che era passato come parametro e self.name = 'Italia'
                # è un attributo della classe
                #
                # probabilmente 'Italia' lo ha preso dal primo campo
                # del file ExampleDelivery/Instances/Nazione.yaml
                d[info_name] = self.name
                distr_info[k] = d
            # è cambiato il formato di distr_info, ha aggiunto la nazione di provenienza del partito
            # NON PERCHE LO ABBIA FATTO
            # formato distr_info, dizionario :
            #                       - chiave : 'nome_parito'
            #                       - valore : dict{ 'Voti' : int_ numero_voti,
            #                                        'Nazione' : 'Italia' }


            # credo che trasformi semplicemente distr_info da un dizionario ad una lista
            info = [distr_info] + list(info)

            rets = []

            # questa istruzione copia spec_info in sub_info
            sub_info = {k: v for k, v in
                        spec_info.items()}  
            # TODO di Ruffati
            # TODO: distinguere gen_info e loc_info, gen info riguarda il livello superiore loc_info riguarda il livello che chiamo
            
            # è cambiato il formato di subb_info, ha aggiunto la nazione di provenienza del partito e del candidato
            # ha fatto la stessa cosa di qualche istruzione precedente
            # CONTINUO A NON CAPIRE PERCHE
            for sub, sub_inf in sub_info.items():
                for k, v in sub_inf.items():
                    v[info_name] = self.name

            for i in subs:
                # qua prende l'istanza della sottoclasse con il nome 'i'
                # nel caso con i dati europei passa le varie istanze di Circoscrizione
                #
                # 'I : ITALIA NORD-OCCIDENTALE'
                # 'II : ITALIA NORD-ORIENTALE'
                # 'III : ITALIA CENTRALE'
                # 'IV : ITALIA MERIDIONALE'
                # 'V : ITALIA INSULARE'
                inst = src.GlobalVars.Hub.get_instance(sub_level, i)

                # IMPORTANTE
                # questa riga genera parte dell'output finale
                #
                # ok, questa riga chiama exec_lane della sottolane
                # in questo caso genera l'output perchè credo che 'Circoscrizione'
                # sia la lane_tail e quindi è l'ultimo step che calcola i dati
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

        # formato lane_name : string        ---> valore con dati europei è 'lista'

        # formato first_input : string      ---> valore con dati europei è 'liste'

        # formato order_number : int       ---> valore con dati europei è 1

        # formato class_name : string       ---> valore con dati europei è 'Nazione'

        # formato kwatgs : dizionario
        # {
        #   'sub_level': 'Circoscrizione', 
        #   'info_name': 'Nazione', 
        #   'operations': [
        #                   {
        #                       'collect_type': 'liste', 
        #                       'ideal_distribution': '$', 
        #                       'corrector': 'Commons.correct_europee'
        #                   }, 
        #                   {
        #                       'collect_type': 'candidati', 
        #                       'ideal_distribution': '$', 
        #                       'corrector': 'Commons.no_op', 
        #                       'forward_distribution': True
        #                   }
        #                 ]
        # }
        #
        # questi dati vengono presi dal file in ExampleDelivery/Classes/Nazione.yaml dalla riga 7
        # da quella riga viene definito tutto :
        # nome lane, order number, tipo di lane, sublevels, operazioni, e tutti i parametri vari


        # questa riga aggiungere la nuova lane alle registro delle lane
        src.GlobalVars.Hub.register_lane(name=lane_name, head_class=class_name, order=order_number)

        # questa riga fa andare la funzione parse_lane_node,
        # la funzione può essere trovata in questo file,
        # parsa le info passate
        #
        # con i valori delle europee ho mcs         ---> src.comb_Nazione
        # con i valore delle europee ho lane_name   ---> lista
        f = mcs.parse_lane_node(lane_name, **kwargs)

        def exec_head(self, lane):
            distribution, info = self.propose(first_input)

            # formato distribution :
            #       indice      partito                     seggi
            #       8           LEGA SALVINI PREMIER        30
            #       12          PARTITO DEMOCRATICO         20
            #...
            #
            # dagli indici possiamo capire che sono gli elementi di una lista
            # piu generale in cui erano presenti tutti i partiti
            # dai dati europei la somma dei seggi ai cinque partiti viene 76
            # quindi è una distribuzione generale, non divisa per subdivisions

            # formato info : dizionario
            #                   - chiave : string_nome_partito
            #                   - valore : dict{ 'Voti' : int_numero_voti_partito }

            # con questa riga sembra restituire il formato di ritorno
            # perchè è la prima parte dell'output, ovvero la distribuzione
            # dei seggi in base alle circoscrizioni
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
        # questa funzione viene chiamata tre volte apparentemente
        # credo sia una per lane, dato che abbbimao tre lane con i dati europei
        # (Nazione, Circoscrizione, Lista)
        #
        # alla prima chiamata ho :
        #               - mcs = src.comb_Circoscrizione
        #               - source = <function source_parse.<locals>.function_returned at instance_address>
        #               - distribution = ['Lista', 'Seggi']
        #               - info = ['Resto']
        #               - kwargs = {}
        #
        # alla seconda chiamata ho :
        #               - mcs = src.comb_Circoscrizione
        #               - source = <function source_parse.<locals>.function_returned at instance_address>
        #               - distribution = ['Candidato', 'Voti']
        #               - info = ['Voti']
        #               - kwargs = {}
        #
        # alla terza chiamata ho :
        #               - mcs = src.comb_Nazione
        #               - source = <function source_parse.<locals>.function_returned at instance_address>
        #               - distribution = ['Partito', 'Seggi']
        #               - info = ['Voti']
        #               - kwargs = {}
        #
        # questi dati sono presi dai rispettivi file in ExampleDelivery/Classes/(Circoscrizione.yaml o Nazione.yaml)
        #
        # guardando il file Circoscrizione.yaml si trova che :
        #       - la prima chiamata riguarda le liste e chiama la funzione 'commons.assign_local_seats'
        #       - la seconda chiamata rigurda i candidati e non chiama funzione
        #
        # guardando il file Nazione.yaml si trova che :
        #       - la terza chiamata chiama la funzione 'self.seggi_lista'
        

        # questo restituisce i dati delle distribuzioni sul dataframe passato
        # in base ai campi di distribuzione richiesti
        def distribution_list(df):
            return df[distribution]

        # qui decidiamo al funzione di distribuzione 
        # e la chiave della distribuzione
        # in base al parametro distribution
        if type(distribution) == list:
            distr_fun = distribution_list
            key_d = distribution[0]
        else:
            # mai usata questa istruzione, quindi non so che fa
            # dovrò analizzare la funzione interessata
            key_d, distr_fun = mcs.parse_propose_distribution_dict(**distribution)
            # distr_fun accetta un dataframe

        # info_key viene utilizzato se la chiave è diversa dalla chiave della distribuzione
        # se non viene assegnata allora gli assegnamo automaticamente la chiave
        # della distribuzione 
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

            # formato kind : string
            #TODO: aggiustare cosa prende la propose, idealmente tra i parametri  ... VEDI AUDIO TELEGRAM

            # MA COSA VUOL DIRE VEDI AUDIO TELEGRAM
            locs = locals()

             # data credo siano i voti ai candidati divisi per circoscrizioni
            data = source(locs, information=information, constraint=constraint, distribution=distribution)

            info_dict = {}

            for _, s in data.iterrows():
                info_dict[s[info_key]] = {k: s[k] for k in info}
            distr_ret = distr_fun(data)

             # qui vengono analizzati i file .yaml e vegnono restituiti le info
            # richieste dalla sezione lanes_propose
            # 
            # info_dict : è un dizionario con 
            #                       - chiave : i valori del primo attributo di lanes_propose
            #                                   (quindi guardando Nazione.yaml sono liste)
            #                       - valore : un dizionario formattato come la sezione info
            #                                   sotto lanes_propose/'attributo'
            #
            # distr_fun : è la funzione usata per la distribuzione (CREDO, DA VERIFICARE)
            #               potrebbe essere la funzione esplicitata nei file ExampleDelivery/Classes/.yaml
            #               alla sezione lanes_propose/'attributo'/source/name
            #
            # distr_ret : è una lista (o array) con i campi formattati secondo quanto esplicitato
            # alla sezione lanes_propose/'attributo'/distribution nei file ExampleDelivery/Classes/.yaml

            distr_ret = distr_ret[distr_ret.iloc[:, 1] > 0].copy()

            # ritorna la distribuzione distr_ret prima dell'ultima istruzione
            # ovvero una distribuzione con i campi formattati secondo quanto esplicitato
            # alla sezione lanes_propose/'attributo'/distribution nei file ExampleDelivery/Classes/.yaml
            #
            # e ritorna anche info_dict, vedi sopra per formato di info_dict
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
