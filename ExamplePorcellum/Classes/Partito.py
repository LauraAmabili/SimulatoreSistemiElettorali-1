import pandas as pd
import numpy as np
import yaml

conf = """
metaclasses:
  - logger # aggiunge automaticamente una funzione log
  - subclass

subclass:
    - PolEnt
"""

conf = """
metaclasses:
    - logger
    - PolEnt
    - party

subclass:
    - PolEnt

sub_of:
    - coalition

party:
    info_vars:
        - coalition

"""





conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)
metas_p
comb_p = type("combPol", tuple(metas_p), {})


class Partito(metaclass=comb_p, **conf):

    
    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        # il dataframe ha le colonne : LISTA COALIZIONE VOTI

        if sbarramenti[0] == 'regione' and district.type == 'Nazione' :

            # solo i partiti che stanno in queste due regione ricevono un
            # filtro regionale, le altre regioni non lo prevedono
            if row['Regione'] == 'TRENTINO-ALTO ADIGE' or row['Regione'] == 'FRIULI-VENEZIA GIULIA' :

                # prendo tutte le righe del partito nelle diverse regioni
                # se riga_cercata ha solo una riga allora il partito si è presentato
                # unicamente in una regione (tra trentino e friuli)
                riga_cercata = dataframe[dataframe['Partito'] == row['Partito']]

                if len(riga_cercata.index) == 1 :
                    tot_voti_regione = dataframe[dataframe['Regione'] == row['Regione']]['Voti'].sum()
                    tot_voti_partito = riga_cercata['Voti'].sum()

                    self.percRegione = (tot_voti_partito / tot_voti_regione) * 100

                    return tot_voti_partito > tot_voti_regione * 0.2
            else :
                self.percRegione = 0.0
            
            return False
                    
                

            

        if sbarramenti[0] == 'elette' and district.type == 'Nazione':

            #print("eseguo filter di partito in ", district.type)

            tot_voti = dataframe['Voti'].sum()
            # calcolo il numero di voti totali del partito
            solo_righe_partito = dataframe[dataframe['Partito'] == row['Partito']]
            tot_voti_partito = solo_righe_partito['Voti'].sum()

            self.percNazione = (tot_voti_partito / tot_voti) * 100
            self.votiPartito = tot_voti_partito

            # questo controllo viene effettuato solo se il partito
            # sta effettivamente dentro ad una coalizione
            #
            # NO COALIZIONE non è una coalizione
            if row['Coalizione'] != 'NO COALIZIONE' :

                # calcolo il numero di voti totali della coalizione
                solo_righe_coalizione = dataframe[dataframe['Coalizione'] == row['Coalizione']]
                tot_voti_coalizione = solo_righe_coalizione['Voti'].sum()

                if tot_voti_coalizione > tot_voti * 0.1 :
                    return True
            
            # se la coalizione non è passata, o se non stava in coalizione,
            # allora controllo direttamente se ha passato il 4% dei voti
            # validi #
            return tot_voti_partito > tot_voti * 0.04

        return True

    



