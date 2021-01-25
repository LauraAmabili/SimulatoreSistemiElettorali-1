import pandas as pd
import yaml
import src.GlobalVars as gv


conf = """
metaclasses:
  - logger
  - subclass

subclass:
    - PolEnt
"""

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)
metas_p
comb_p = type("combPol", tuple(metas_p), {})


class Coalizione(metaclass=comb_p, **conf):

    
    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        # il dataframe ha le colonne : COALIZIONE LISTA VOTI #

        # controllo il numero dei voti solo a livello nazione perchè non ci sono
        # filtri a livello regionale per le coalizioni #
        if sbarramenti[0] == 'elette' and district.type == 'Nazione':
            
            #print("eseguo filter di coalizione in ", district.type)

            if row['Coalizione'] == 'NO COALIZIONE' :
                return False
            
            tot_voti = dataframe['Voti'].sum()
            tot_voti_coalizione = row['Voti']

            return tot_voti_coalizione > tot_voti * 0.1

        return True


    def get_partiti_spettanti_seggi(self) :

        partiti = gv.Hub.get_political_subs(self, 'PolEnt')
        percentuali_regionali_partiti = {}
        percentuali_nazionali_partiti = {}

        # riempio dizionari delle percentuali dei voti presi nella classe party#
        for partito in partiti :
            istanza_partito = gv.Hub.get_instance('PolEnt', partito)
            percentuali_nazionali_partiti[partito] = istanza_partito.percNazione
            percentuali_regionali_partiti[partito] = istanza_partito.percRegione
        
        # sorto le percentuali nazionali (mi serve per prendere miglior_perdente) #
        percentuali_nazionali_partiti = dict(sorted(percentuali_nazionali_partiti.items(), key=lambda item: item[1], reverse=True))

        partiti_spettanti_seggi = []
        prendi_miglior_perdente = False

        # prendo partiti che hanno superato soglia 2% e miglior perdente #
        for partito in percentuali_nazionali_partiti.keys() :
            
            if percentuali_nazionali_partiti.get(partito) > 2. :
                partiti_spettanti_seggi.append(partito)
                prendi_miglior_perdente = True
            elif prendi_miglior_perdente :
                partiti_spettanti_seggi.append(partito)
                prendi_miglior_perdente = False

        # prendo partiti che hanno superato soglia regionale in trentino e friuli
        # 20% voti regionali #
        for partito in percentuali_regionali_partiti.keys() :

            if percentuali_regionali_partiti.get(partito) > 20. :
                if partito not in partiti_spettanti_seggi :
                    partiti_spettanti_seggi.append(partito)

        return partiti_spettanti_seggi