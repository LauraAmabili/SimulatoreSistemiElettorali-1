import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import src.GlobalVars as gv
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

pd.options.mode.chained_assignment = None


# SEZIONE DISTRIBUZIONE <-------------------------------------------------------- #


def distrib_porcellum(*a, data, seats, df_partiti_filtrato, df_partiti_regioni, premio_maggioranza, **kwargs):

    print("\n---> TROVO LA DISTRIBUZIONE DEI SEGGI NAZIONALI <---\n")

    # df_coalizioni è un dataframe che contiene le coalizioni
    # che hanno passato la soglia di sbarramento del 10% (per il porcellum)
    # e il numero di voti presi per ogni coalizione
    # (è compresa anche la coalizione NO COALIZIONE, che racchiude tutti
    # i partiti non facenti parte di una coalizione effettiva)
    #
    # 
    # df_partiti è un dataframe che contiene i partiti
    # che hanno passato la soglia di sbarramento del 4% (per il porcellum)
    # o che fanno parte di una coalizione che ha passato lo sbarramento
    # e il numero di voti presi per ogni partito#
    df_coalizioni = data.copy()
    df_partiti = df_partiti_filtrato.copy()

    lista_coalizioni_passate = df_coalizioni['Eleggibile'].unique()

    df_partiti_passati = df_partiti[~df_partiti['Coalizione'].isin(lista_coalizioni_passate)]

    df_da_concatenare = [df_coalizioni, df_partiti_passati]
    df_eleggibili = pd.concat(df_da_concatenare)
    df_eleggibili = df_eleggibili.drop(['Coalizione'], axis=1)



    # Q è la somma di tutti i voti diviso per il numero di seggi generali
    tot_voti = int(df_eleggibili['Votes'].sum())
    q = int(tot_voti / seats)

    # // è la divisione che arrotonda all'intero inferiore
    # e nella riga dopo casto il campo Seats a int
    df_eleggibili['Seats'] = df_eleggibili['Votes'] // q
    df_eleggibili['Seats'] = df_eleggibili['Seats'].astype("int")

    # il campo Remainder e il "resto"
    df_eleggibili['Remainder'] = df_eleggibili['Votes'] / q - df_eleggibili['Seats']
    # il campo RemainderUsed indica se il resto è stato usato
    df_eleggibili['RemainderUsed'] = False

    # R sono i seggi rimanenti che non sono stati assegnati
    # e che verranno assegnati con i resti #
    r = seats - df_eleggibili['Seats'].sum()

    # qua ordino i partiti in base al resto
    df_eleggibili.sort_values('Remainder', ascending=False, inplace=True)

    # assegno i seggi rimanenti
    df_eleggibili.iloc[:r, df_eleggibili.columns.get_loc('RemainderUsed')] = True
    df_eleggibili.iloc[:r, df_eleggibili.columns.get_loc('Seats')] += 1

    # qua ordino i partiti in base al numero di voti che hanno preso
    df_eleggibili.sort_values('Votes', ascending=False, inplace=True)

    # se il partito che ha preso piu voti non ha raggiunto i 340 seggi
    # allora glieli assegno automaticamente #

    # in questa parte vado ad assegnare il premio di maggioranza al
    # partito che ha preso piu voti, ma solo se non ha raggiunti i 340 seggi
    if df_eleggibili.iloc[0, df_eleggibili.columns.get_loc('Seats')] < premio_maggioranza :
       

        df_eleggibili.iloc[0, df_eleggibili.columns.get_loc('Seats')] = premio_maggioranza

        # Q è la somma di tutti i voti diviso per il numero di seggi generali
        #data2 = data.copy()
        df_eleggibili_2 = df_eleggibili.iloc[1:]

        remainingSeats = seats - df_eleggibili.iloc[0, df_eleggibili.columns.get_loc('Seats')].item()
        q = int(df_eleggibili_2['Votes'].sum() / remainingSeats)

        # // è la divisione che arrotonda all'intero inferiore
        # e nella riga dopo casto il campo Seats a int
        df_eleggibili_2['Seats'] = df_eleggibili_2['Votes'] // q
        df_eleggibili_2['Seats'] = df_eleggibili_2['Seats'].astype("int")

        # il campo Remainder e il "resto"
        df_eleggibili_2['Remainder'] = df_eleggibili_2['Votes'] / q - df_eleggibili_2['Seats']
        # il campo RemainderUsed indica se il resto è stato usato
        df_eleggibili_2['RemainderUsed'] = False

        # R sono i seggi rimanenti che non sono stati assegnati
        # e che verranno assegnati con i resti #
        r = remainingSeats - df_eleggibili_2['Seats'].sum()

        # qua ordino i partiti in base al resto
        df_eleggibili_2.sort_values('Remainder', ascending=False, inplace=True)

        # assegno i seggi rimanenti
        df_eleggibili_2.iloc[:r, df_eleggibili.columns.get_loc('RemainderUsed')] = True
        df_eleggibili_2.iloc[:r, df_eleggibili.columns.get_loc('Seats')] += 1

        # qua ordino i partiti in base al numero di voti che hanno preso
        df_eleggibili_2.sort_values('Votes', ascending=False, inplace=True)
        
        df_eleggibili_2.loc[df_eleggibili.index[0]] = df_eleggibili.iloc[0]
        df_eleggibili_2.sort_values('Seats', ascending=False, inplace=True)

        df_eleggibili = df_eleggibili_2.copy()

    #print('DISTRIBUZIONE FINALE CON PORCELLUM ')
    print(df_eleggibili)


    print("\n->SUDDIVIDO I SEGGI TRA I PARTITI<-\n")
    df_nazionale_partiti = dividi_per_partiti(df_eleggibili, df_partiti, df_coalizioni)
    print(df_nazionale_partiti)

    return df_nazionale_partiti


def distrib_porcellum_aosta(*a, data, **kwargs):
    #print("\n---> ELEGGO IL SEGGIO DELLA VALLE D'AOSTA <---\n")

    df_seggi_aosta = data.copy()

    df_seggi_aosta.sort_values('Voti', ascending=False, inplace=True)

    df_seggi_aosta['Seggi'] = 0

    df_seggi_aosta.iloc[0, df_seggi_aosta.columns.get_loc('Seggi')] = 1
    df_seggi_aosta.iloc[1:, df_seggi_aosta.columns.get_loc('Seggi')] = 0

    df_seggi_aosta = df_seggi_aosta.rename(columns={'Voti': 'Numero'})

    #print(df_seggi_aosta)

    return df_seggi_aosta


def distrib_porcellum_estero(*a, seats, data, **kwargs):

    df_estero = data.copy()
    df_estero['Seggi'] = 0

    return df_estero


# SEZIONE DIVISIONE <-------------------------------------------------------- #


def dividi_per_partiti(df_eleggibili, df_partiti, df_coalizioni):
    
    # per ogni riga di eleggibili (quindi quello contente sia coalizioni che partiti)
    # devo controllare se l'eleggibile è un partito o coalizione, se quest'ultima
    # allora devo guardare tra il df_partiti quali sono quelli che possono prendere
    # seggi in base allo sbarramento del 2% e suddividere i seggi della coalizione tra
    # i partiti
    # #
    lista_coalizioni_elette = df_coalizioni['Eleggibile'].unique()

    frame = []

    for index, row_eleggibili in df_eleggibili.iterrows() :

        # se questa riga di df_eleggibile è una coalizione
        # allora devo distribuire i seggi ai partiti sottostanti
        # altrimenti do il numero di seggi direttamente al partito
        # #
        if row_eleggibili['Eleggibile'] in lista_coalizioni_elette :
            
            coalizione = row_eleggibili['Eleggibile']
            seggi_coalizione = row_eleggibili['Seats']

            partiti_spettanti_seggi = gv.Hub.get_instance('PolEnt', coalizione).get_partiti_spettanti_seggi()
            df_partiti_in_coalizione = df_partiti[df_partiti['Eleggibile'].isin(partiti_spettanti_seggi)]
            df_partiti_in_coalizione['Coalizione'] = row_eleggibili['Eleggibile']

            tot_voti_coalizione_suddivisione = df_partiti_in_coalizione['Votes'].sum()
            q = int(tot_voti_coalizione_suddivisione / seggi_coalizione)
            

            df_partiti_in_coalizione['Seats'] = df_partiti_in_coalizione['Votes'] // q
            df_partiti_in_coalizione['Seats'] = df_partiti_in_coalizione['Seats'].astype("int")

            df_partiti_in_coalizione['Remainder'] = df_partiti_in_coalizione['Votes'] / q - df_partiti_in_coalizione['Seats']
            df_partiti_in_coalizione['RemainderUsed'] = False

            seggi_rimanenti = seggi_coalizione - df_partiti_in_coalizione['Seats'].sum()

            # qua ordino i partiti in base al resto
            df_partiti_in_coalizione.sort_values('Remainder', ascending=False, inplace=True)

            # assegno i seggi rimanenti
            df_partiti_in_coalizione.iloc[:seggi_rimanenti, df_partiti_in_coalizione.columns.get_loc('RemainderUsed')] = True
            df_partiti_in_coalizione.iloc[:seggi_rimanenti, df_partiti_in_coalizione.columns.get_loc('Seats')] += 1

            df_partiti_in_coalizione.sort_values('Seats', ascending=False, inplace=True)

            
            # ho assegnato tutti i seggi ai partiti di una coalizione quindi ora appendo alla distribuzione finale
            # e passo alla prossima row_eleggibili
            frame.append(df_partiti_in_coalizione)
        
        else :
            df_partito = df_eleggibili[df_eleggibili['Eleggibile'] == row_eleggibili['Eleggibile']]
            df_partito['Coalizione'] = 'NO COALIZIONE'
            frame.append(df_partito)
    
    # END-FOR
    df_distribuzione_finale = pd.concat(frame)

    # tolto e rinnomino colonne # 
    df_distribuzione_finale = df_distribuzione_finale.drop(['Remainder', 'RemainderUsed'], axis=1)
    df_distribuzione_finale = df_distribuzione_finale.rename({'Eleggibile': 'Partito'}, axis=1)


    # questa parte mi aggiunge il numero di voti totali che la coalizione ha preso
    # comprendendo anche i voti delle liste della coalizione che non hanno preso seggi #
    df_distribuzione_finale['VotiCoalizione'] = 0
    for index, row in df_distribuzione_finale.iterrows():
        if row['Coalizione'] == 'NO COALIZIONE':
            voti_coal =  int(df_eleggibili[df_eleggibili['Eleggibile'] == row['Partito']]['Votes'])
        else :
            voti_coal = int(df_eleggibili[df_eleggibili['Eleggibile'] == row['Coalizione']]['Votes'])
        
        df_distribuzione_finale.at[index, 'VotiCoalizione'] = voti_coal
    

    return df_distribuzione_finale


def divisione_circoscrizionale_seggi(*, information, distribution, district_votes, seggi, **kwargs):

    # FORMATO distribution :
    # dataframe con le colonne Partito, Seggi, Coalizione
    # 
    # contiene il numero di seggi assegnato a livello nazionale ad ogni partito
    # e la coalizione di cui il partito fa parte #

    # FORMATO district_votes :
    # dataframe con le colonne Partito, Coalizione, Voti
    # 
    # contiene il numero di voti che ogni partito ha preso 
    # a livello circoscrizionale e la coalizione di cui fa parte #

    # FORMATO voti_nazionali :
    # dizionario con la seguente indentazione
    # { 'nome_partito': { 'Voti': int_numero_voti }}
    # 
    # contiene il numero di voti presi a livello nazionale da ogni partito #

    # cosa fare
    # allora devo identificare la coalizione/partito di maggioranza
    # calcolare il suo numero di voti nazionali e poi il quoziente nazionale di maggioranza
    # 
    # poi per i partiti di minoranza devo calcolare un unico quoziente nazionale di minoranza #

    numero_seggi_nazione = distribution['Seggi'].sum()

    tot_voti_nazione = (distribution['VotiCoalizione'].unique()).sum()
    tot_voti_maggioranza = 0
    tot_voti_minoranza = 0

    numero_seggi_circoscrizione = seggi[0]

    # lista_coalizioni_pariti è la lista che contiene 
    # le coalizioni e partiti che hanno preso dei seggi 
    # nella lista non sono presenti i partiti dentro ad una coalizione
    # perchè viene presa la coalizione nel complesso #
    lista_coalizioni_partiti = distribution['Coalizione'].unique()
    lista_coalizioni_partiti = np.delete(lista_coalizioni_partiti, np.argwhere(lista_coalizioni_partiti=='NO COALIZIONE'))
    lista_coalizioni_partiti = np.append(lista_coalizioni_partiti, distribution[distribution['Coalizione'] == 'NO COALIZIONE']['Partito'].unique())

    
    dizionario_quozienti_mag_min = {}
    eleggibile_di_maggioranza = ''
    for elem in lista_coalizioni_partiti:
    
        seggi = 0

        df_elem = distribution[distribution['Coalizione'] == elem]
        if len(df_elem) == 0 :
            df_elem = distribution[distribution['Partito'] == elem]
        
        seggi = df_elem['Seggi'].sum()
        # se ho trovato la coalizione/partito di maggioranza
        # allora mi salvo il nome per verificarlo dopo
        # calcolo il suo numero di voti nazionali
        # 
        # dal numero di voti nazionali di maggioranza deduco il numero
        # di voti di minoranza nazionali e il numero di seggi per il
        # successivo calcolo del quoziente nazionale di minoranza #
        if seggi >= 340 :

            # qui ho trovato la coalizione/partito di maggioranza,
            # salvo il nome per verificarlo dopo #
            eleggibile_di_maggioranza = elem

            # prendo il numero dei voti totali della coalizione/partito di maggioranza 
            # e calcolo il quoziente nazionale di maggioranza #
            tot_voti_maggioranza = df_elem['VotiCoalizione'].unique()
            dizionario_quozienti_mag_min['Maggioranza'] = tot_voti_maggioranza // seggi

            # ora calcolo il numero dei voti totali della minoranza e calcolo
            # il quoiente nazionale di minoranza #
            tot_voti_minoranza = tot_voti_nazione - tot_voti_maggioranza
            seggi_minoranza = distribution['Seggi'].sum() - seggi
            dizionario_quozienti_mag_min['Minoranza'] = tot_voti_minoranza // seggi_minoranza
        

    # il dataframe per la distribuzione dei seggi a livello circoscrizionale #
    distribuzione_circ = pd.DataFrame(lista_coalizioni_partiti, columns= ['Eleggibile'])
    distribuzione_circ['Seggi'] = 0
    distribuzione_circ['Indice'] = 0
    distribuzione_circ['Voti_Circ'] = 0
    distribuzione_circ['Resto'] = 0
    distribuzione_circ['Resto_Usato'] = False

    for elem in lista_coalizioni_partiti:

        tot_voti_circ = 0
        indice_relativo = 0

        df_elem = district_votes[district_votes['Coalizione'] == elem]
        if len(df_elem) > 0 :
             tot_voti_circ = df_elem['Voti'].sum()
        else:
            df_elem = district_votes[district_votes['Partito'] == elem]
            tot_voti_circ = int(df_elem['Voti'])
        
        # qui decido quale quoziente nazionale usare (maggioranza o minoranza) #
        quoziente = 0
        if elem == eleggibile_di_maggioranza:
            quoziente = dizionario_quozienti_mag_min['Maggioranza']
        else:
            quoziente = dizionario_quozienti_mag_min['Minoranza']
        
        # calcolo indice relativo per l'assegnazione dei seggi #
        indice_relativo = tot_voti_circ / quoziente

        i = distribuzione_circ.index[distribuzione_circ['Eleggibile'] == elem].tolist()
        distribuzione_circ['Voti_Circ'][i] = tot_voti_circ
        distribuzione_circ['Indice'][i] = indice_relativo
    
    somma_indici = distribuzione_circ['Indice'].sum()

    distribuzione_circ['Seggi'] = (distribuzione_circ['Indice'] * numero_seggi_circoscrizione) // somma_indici
    distribuzione_circ['Resto'] = ((distribuzione_circ['Indice'] * numero_seggi_circoscrizione) / somma_indici) - distribuzione_circ['Seggi']
    distribuzione_circ['Seggi'] = distribuzione_circ['Seggi'].astype("int")
    
    # calcolo dei seggi restanti per la distribuzione con metodo dei piu alti resti #
    seggi_restanti = numero_seggi_circoscrizione - distribuzione_circ['Seggi'].sum()

    distribuzione_circ.sort_values('Resto', ascending=False, inplace=True)
    distribuzione_circ.reset_index(drop=True, inplace=True)

    for i in range(seggi_restanti):
        distribuzione_circ['Resto_Usato'][i] = True
        seggi_new = int(distribuzione_circ['Seggi'][i]) + 1
        distribuzione_circ['Seggi'][i] = seggi_new


    return distribuzione_circ


def divisione_circoscrizionale_partiti(*, information, distribution, district_votes, seggi, distretto, **kwargs):

    lista_partiti = information[1].keys() # lista dei partiti spettanti di seggi #

    lista_coalizioni = district_votes['Coalizione'].unique()
    lista_coalizioni = np.delete(lista_coalizioni, np.argwhere(lista_coalizioni=='NO COALIZIONE')) # lista coalizioni spettanti di seggi #

    numero_seggi_circoscrizione = seggi[0]

    district_votes_filtrato = district_votes[district_votes['Partito'].isin(lista_partiti)]
    lista_partiti_circoscrizione = district_votes_filtrato['Partito'].unique()

    lista_partiti_senza_coal = district_votes_filtrato[district_votes_filtrato['Coalizione'] == 'NO COALIZIONE']['Partito'].unique()
    lista_partiti_senza_coal = [value for value in lista_partiti_senza_coal if value in lista_partiti] # lista di partiti non in coalizioni spettanti seggi in questa circoscrizione #
    
    distribuzione_coalizioni_circ = distribution.get(distretto)

    # voti_coalizioni, dizionario :
    #   - chiave : nome coalizione
    #   - valore : dizionario con chiavi Voti, Seggi, Quoziente
    info_coalizioni = {}
    for elem in lista_coalizioni:
        info = {'Voti' : 0, 'Seggi' : 0, 'Quoziente' : 0}

        tot_voti_coalizione = district_votes_filtrato[district_votes_filtrato['Coalizione'] == elem]['Voti'].sum()
        info['Voti'] = tot_voti_coalizione
        info['Seggi'] = int(distribuzione_coalizioni_circ[distribuzione_coalizioni_circ['Eleggibile'] == elem]['Seggi'])
        if info['Seggi'] > 0 :
            info['Quoziente'] = info['Voti'] // info['Seggi']

        info_coalizioni[elem] = info
    
    #print(info_coalizioni)

    
    # per ogni coalizione devo dividere i seggi #
    frame = []
    for coal, info in info_coalizioni.items():
        distrib_coal = district_votes_filtrato[district_votes_filtrato['Coalizione'] == coal]
        distrib_coal['Seggi'] = 0
        distrib_coal['Resto'] = 0
        distrib_coal['Resto_Usato'] = False

        if info['Quoziente'] == 0 :
            continue

        distrib_coal['Seggi'] = distrib_coal['Voti'] // info['Quoziente']
        distrib_coal['Seggi'] = distrib_coal['Seggi'].astype("int")
        distrib_coal['Resto'] = (distrib_coal['Voti'] / info['Quoziente']) - distrib_coal['Seggi']

        restanti = info['Seggi'] - distrib_coal['Seggi'].sum()
        distrib_coal.sort_values('Resto', ascending=False, inplace=True)

        distrib_coal.iloc[:restanti, distrib_coal.columns.get_loc('Resto_Usato')] = True
        distrib_coal.iloc[:restanti, distrib_coal.columns.get_loc('Seggi')] += 1
        distrib_coal.sort_values('Seggi', ascending=False, inplace=True)

        frame.append(distrib_coal)
    
    for partito in lista_partiti_senza_coal:
        row_partito = distribuzione_coalizioni_circ[distribuzione_coalizioni_circ['Eleggibile'] == partito]
        row_partito.rename(columns={'Voti_Circ': 'Voti'}, inplace=True)
        row_partito['Partito'] = partito
        row_partito['Coalizione'] = 'NO COALIZIONE'
        row_partito['Resto'] = 0
        row_partito['Resto_Usato'] = False

        frame.append(row_partito)

    
    distrib_seggi_partiti = pd.concat(frame)

    return distrib_seggi_partiti



# SEZIONE CORREZIONE <-------------------------------------------------------- #


def correct_porcellum(distretto, distribuzione_ideale, distribuzione_raccolta,
                    info_locali, *info_comuni):

    print("\n-> SUDDIVISIONE CIRCOSCRIZIONALE DEI SEGGI ASSEGNATI <-\n")
    
    lista_coalizioni_partiti = distribuzione_ideale['Coalizione'].unique()
    lista_coalizioni_partiti = np.delete(lista_coalizioni_partiti, np.argwhere(lista_coalizioni_partiti=='NO COALIZIONE'))
    lista_coalizioni_partiti = np.append(lista_coalizioni_partiti, distribuzione_ideale[distribuzione_ideale['Coalizione'] == 'NO COALIZIONE']['Partito'].unique())


    lista_seggi_assegnati = {}
    lista_seggi_eccedenti = {}

    
    for elem in lista_coalizioni_partiti :

        tot_seggi_assegnati_circ = 0

        for distrib_circ in distribuzione_raccolta.values() :
            tot_seggi_assegnati_circ += int(distrib_circ[distrib_circ['Eleggibile'] == elem]['Seggi'])
        
        lista_seggi_assegnati[elem] = tot_seggi_assegnati_circ

        numero_seggi_coalizione_partito = distribuzione_ideale[distribuzione_ideale['Coalizione'] == elem]['Seggi'].sum()
        if numero_seggi_coalizione_partito == 0 :
            numero_seggi_coalizione_partito = distribuzione_ideale[distribuzione_ideale['Partito'] == elem]['Seggi'].sum()

        lista_seggi_eccedenti[elem] = tot_seggi_assegnati_circ - numero_seggi_coalizione_partito
    
    lista_seggi_eccedenti = dict(sorted(lista_seggi_eccedenti.items(), key=lambda item: item[1], reverse=True))

    #print(lista_seggi_eccedenti)
    eleggibili_seggi_mancanti = {}
    eleggibili_seggi_eccedenti = {}

    for eleggibile, seggi in lista_seggi_eccedenti.items() :
        if seggi < 0:
            eleggibili_seggi_mancanti[eleggibile] = seggi
        elif seggi > 0:
            eleggibili_seggi_eccedenti[eleggibile] = seggi
    
    lista_info_eleggibili = {}

    for eleggibile, seggi_eccedenti in eleggibili_seggi_eccedenti.items() :
        
        dict_info_circ = {}
        for circ, distrib_circ in distribuzione_raccolta.items():

            # Prendo solo dove i seggi vengono assegnati grazie alla parte decimale 
            # se non ho assegnato un seggio grazie alla parte decimale non includo le info #
            if distrib_circ[distrib_circ['Eleggibile'] == eleggibile]['Resto_Usato'].item() == True :
                dict_info_distribuzione = {}
                dict_info_distribuzione['Seggi'] = int(distrib_circ[distrib_circ['Eleggibile'] == eleggibile]['Seggi'])
                dict_info_distribuzione['Resto'] = distrib_circ[distrib_circ['Eleggibile'] == eleggibile]['Resto'].item()

                dict_info_circ[circ] = dict_info_distribuzione

        dict_info_circ = dict(sorted(dict_info_circ.items(), key=lambda item: item[1].get('Resto'), reverse=False))
        lista_info_eleggibili[eleggibile] = dict_info_circ

    
    
    for eleggibile, seggi_eccedenti in eleggibili_seggi_eccedenti.items() :
        info_resti_coal = lista_info_eleggibili.get(eleggibile, {})

        for circ in info_resti_coal.keys():
                # se la coalizione ha ancora seggi eccedenti allora continuo a toglierli#
                distrib_circ = distribuzione_raccolta.get(circ)
                i_eccedenti = distrib_circ.index[distrib_circ['Eleggibile'] == eleggibile].tolist()

                if distrib_circ['Seggi'][i_eccedenti].item() > 0:

                    df_eleggibile_seggi_mancanti = distrib_circ[distrib_circ['Eleggibile'].isin(eleggibili_seggi_mancanti.keys())]
                    df_eleggibile_seggi_mancanti = df_eleggibile_seggi_mancanti[df_eleggibile_seggi_mancanti['Resto_Usato'] == False]
                    df_eleggibile_seggi_mancanti.sort_values('Resto', ascending=False, inplace=True)

                    if len(df_eleggibile_seggi_mancanti) > 0:
                        eleggibile_assegnatario_seggio = df_eleggibile_seggi_mancanti.iloc[0]['Eleggibile']
                        i_mancanti = distrib_circ.index[distrib_circ['Eleggibile'] == eleggibile_assegnatario_seggio].tolist()

                        distrib_circ['Seggi'][i_eccedenti] -= 1
                        distrib_circ['Seggi'][i_mancanti] += 1

                        eleggibili_seggi_eccedenti[eleggibile] -= 1
                        eleggibili_seggi_mancanti[eleggibile_assegnatario_seggio] += 1

                        if eleggibili_seggi_mancanti[eleggibile_assegnatario_seggio] == 0:
                            eleggibili_seggi_mancanti.pop(eleggibile_assegnatario_seggio, None)
                        if eleggibili_seggi_eccedenti[eleggibile] == 0:
                            break;
    

    for circ, distr in distribuzione_raccolta.items():
        print(circ)
        print(distr)
        print()
    
    # restituisco la nuova distribuzione circoscrizionale
    seggi_coal = {}
    for _,row in distribuzione_ideale.iterrows():
        dict_seggi = {'Seggi': row['Seggi']}
        seggi_coal[row['Partito']] = dict_seggi

    ret = distribuzione_raccolta, {}, seggi_coal

    return ret


def correct_porcellum_partiti(distretto, distribuzione_ideale, distribuzione_raccolta,
                    info_locali, *info_comuni):

    print('\n-> DIVIDO I SEGGI DELLE COALIZIONI TRA I PARTITI CHE NE FANNO PARTE <-\n')

    # lista dei nomi dei partiti che devono prendere dei seggi #
    lista_partiti = info_comuni[0].keys()

    # inizializzo due dizionari che mi serviranno 
    # per salvarmi i partiti e quanti seggi hanno ricevuto in totale 
    # e quanti seggi in piu o in meno hanno 
    # ricevuto rispetto alla distribuzione ideale #
    lista_seggi_assegnati = dict.fromkeys(lista_partiti, 0)
    lista_differenza_seggi = dict.fromkeys(lista_partiti, 0)

    # calcolo il numero totale dei seggi assegnati ad ogni partito 
    # dalla distribuzione che ho ricevuto#
    for circ, distr in distribuzione_raccolta.items():
        for _, row in distr.iterrows():
            lista_seggi_assegnati[row['Partito']] += row['Seggi']
    
    # calcolo la differenza con gli effettivi seggi che ogni 
    # partito doveva prendere in base alla distribuzione nazionale
    # e ordino la lista in modo decrescente #
    for partito, seggi_assegnati in lista_seggi_assegnati.items():
        lista_differenza_seggi[partito] = lista_seggi_assegnati[partito] - info_comuni[0][partito].get('Seggi')
    lista_differenza_seggi = dict(sorted(lista_differenza_seggi.items(), key=lambda item: item[1], reverse=True))


    # due dizionari che mi serviranno per dividere 
    # chi deve cedere e chi deve ricevere seggi #
    lista_seggi_mancanti = {}
    lista_seggi_eccedenti = {}
    for partito, seggi in lista_differenza_seggi.items() :
        if seggi < 0:
            lista_seggi_mancanti[partito] = seggi
        elif seggi > 0:
            lista_seggi_eccedenti[partito] = seggi

    # qui per ogni partito che deve cedere dei seggi controllo dove 
    # gli viene assegnato un seggio usando la parte la decimale (quindi il resto),
    # mi salvo in quale circoscrizione, il valore del resto 
    # e il numero di seggi che ha in quella circoscrizione
    # poi ordino in modo crescente rispetto ai seggi perchè 
    # dovrò cominciare a toglierlo dalla circoscrizione col resto piu basso #
    lista_info_partiti = {}
    for partito, seggi_eccedenti in lista_seggi_eccedenti.items() :
        
        dict_info_circ = {}
        for circ, distrib_circ in distribuzione_raccolta.items():

            lunghezza = len(distrib_circ[distrib_circ['Partito'] == partito]['Resto_Usato'])
            if lunghezza > 0 and distrib_circ[distrib_circ['Partito'] == partito]['Resto_Usato'].item() == True:
                dict_info_distribuzione = {}
                dict_info_distribuzione['Seggi'] = int(distrib_circ[distrib_circ['Partito'] == partito]['Seggi'])
                dict_info_distribuzione['Resto'] = distrib_circ[distrib_circ['Partito'] == partito]['Resto'].item()

                dict_info_circ[circ] = dict_info_distribuzione

        dict_info_circ = dict(sorted(dict_info_circ.items(), key=lambda item: item[1].get('Resto'), reverse=False))
        lista_info_partiti[partito] = dict_info_circ

    
    # qui avviene l'effettivo controllo ed eventuale riassegnamento dei seggi,
    # passando ogni partito che deve cedere dei seggi, controllo se nella circoscrizione 
    # in cui ha ottenuto un seggio grazie alla parte decimale ci sia
    # un partito a cui mancano dei seggi e che non ha ottenuto il seggio tramite la 
    # parte decimale (se ci sono piu seggi con questa condizione perdo quello col il resto piu alto)
    # 
    # successivamente segnalo che al partito è stato assegnato un 
    # seggio con la parte decimale e tolto il segnale a quello a cui è stato tolto #
    for partito, seggi_eccedenti in lista_seggi_eccedenti.items() :
        info_resti_partito = lista_info_partiti.get(partito, {})

        for circ in info_resti_partito.keys():
                # se la coalizione ha ancora seggi eccedenti allora continuo a toglierli#
                distrib_circ = distribuzione_raccolta.get(circ)
                distrib_circ.reset_index(drop=True, inplace=True)

                i_eccedenti = distrib_circ.index[distrib_circ['Partito'] == partito].tolist()

                if distrib_circ['Seggi'][i_eccedenti].item() > 0:

                    df_partiti_seggi_mancanti = distrib_circ[distrib_circ['Partito'].isin(lista_seggi_mancanti.keys())]
                    df_partiti_seggi_mancanti = df_partiti_seggi_mancanti[df_partiti_seggi_mancanti['Resto_Usato'] == False]
                    df_partiti_seggi_mancanti.sort_values('Resto', ascending=False, inplace=True)

                    if len(df_partiti_seggi_mancanti) > 0:
                        partito_assegnatario_seggio = df_partiti_seggi_mancanti.iloc[0]['Partito']
                        i_mancanti = distrib_circ.index[distrib_circ['Partito'] == partito_assegnatario_seggio].tolist()

                        distrib_circ['Seggi'][i_eccedenti] -= 1
                        distrib_circ['Seggi'][i_mancanti] += 1
                        distrib_circ['Resto_Usato'][i_mancanti] = True
                        
                        lista_seggi_eccedenti[partito] -= 1
                        lista_seggi_mancanti[partito_assegnatario_seggio] += 1

                        if lista_seggi_mancanti[partito_assegnatario_seggio] == 0:
                            lista_seggi_mancanti.pop(partito_assegnatario_seggio, None)
                        if lista_seggi_eccedenti[partito] == 0:
                            break;
                        

    # devo ritornare solo la distribuzione, niente altre informazioni #
    ret = distribuzione_raccolta, {}, {}

    # print per una decente visualizzazione della distribuzione finale #
    for circ, distr in ret[0].items() :
        print(circ)
        print(distr)
        print()

    return ret


def correct_porcellum_estero(distretto, distribuzione_ideale, distribuzione_raccolta,
                    info_locali, *info_comuni):

    lista_partiti = distribuzione_ideale['Lista'].unique()

    ideale = pd.DataFrame(lista_partiti, columns =['Lista'])
    ideale['Seggi'] = 0
    ideale['Voti'] = 0

    # con il primo for scorro le circoscrizioni
    # con il secondo for scorro le righe della distribuzine dentro la circoscirizione
    for key, value in distribuzione_raccolta.items() :
        for index, row in value.iterrows() :

            lista = row['Lista']
            
            numero_seggi = row['Seggi']
            seggi_avuti = int(ideale[ideale['Lista'] == lista]['Seggi'])
            new_seggi = seggi_avuti + numero_seggi

            i = ideale.index[ideale['Lista'] == lista].tolist()

            ideale['Seggi'][i] = new_seggi
    
    
    ideale.sort_values('Seggi', ascending=False, inplace=True)
    
    #print("\n---> DISTRIBUZIONE DEI SEGGI ESTERI <---\n")
    #print(ideale)

    ret = distribuzione_raccolta, {}, {}
    return ret


# SEZIONE VISUALIZZAZIONE <-------------------------------------------------------- #

def printing_visuals(lista) :

    
    try: 
        dataset = pd.DataFrame(lista, columns =['Circoscrizione', 'Lane', 'Partito', 'Seggi'])
        dataset['Seggi'] = dataset['Seggi'].astype(int)
    except: 
        print('Dati non formattati per output visuale')
        return 0 

    listaLane = dataset['Lane'].unique()
    print(listaLane)
    


    for lane in listaLane: 

        dataSeggi = dataset.filter(items=['Lane', 'Partito', 'Seggi'])
        dataSeggi = dataSeggi.loc[dataset['Lane'] == lane]
        dataSeggi = dataSeggi.groupby(['Partito'])['Seggi'].sum().reset_index()
        dataSeggi.sort_values('Seggi', ascending = False, inplace = True)
        dataSeggi =  dataSeggi.reset_index()
        dataSeggi = dataSeggi.drop('index', axis=1)

        if lane == 'lista':
            dataPartitoSeggi = dataSeggi.copy()
        print(lane)
        print(dataSeggi)


    #----------> OUTPUT PARTITI
    
    dataOutput = dataset.filter(items=['Lane', 'Partito', 'Seggi'])
    dataOutput = dataOutput.groupby(['Partito'])['Seggi'].sum().reset_index()
    dataOutput.sort_values('Seggi', ascending = False, inplace = True)
    dataOutput =  dataOutput.reset_index()
    dataOutput = dataOutput.drop('index', axis=1)

    dataOutput = dataOutput[dataOutput['Seggi']>0]
    print(dataOutput)

#
   # raw_data = {'NomeLista': dataOutput['Partito'], 
   #     'Seats': dataOutput['Seggi']}
   # 
   # df = pd.DataFrame(raw_data, columns = ['NomeLista', 'Seats'])
   # df['Total_Seats'] = df['Seats'].sum()
#
   #
#
   # #plt.figure(figsize=(15,9))
   # plt.frame.Maximize(True)
   # ax1 = plt.subplot(131, aspect='auto')
#
   # plt.pie(df['Seats'])
   # #colors = ['#191970','#001CF0','#0038E2','#0055D4','#0071C6','#008DB8','#00AAAA','#00C69C','#00E28E','#00FF80',]
   # dataOutput.plot(kind='pie', y = 'Seggi',ax=ax1,
   #  startangle=10, shadow=False,  fontsize=12, autopct='%1.1f%%', title="Divisione Nazionale Camera dei Deputati")
   #
   # plt.legend(labels=['Sticazzi', 'ciao'],loc="upper left")
   # 
   # #fig = px.pie(dataOutput, values='Seggi', names='Partito', title='Divisione Nazionale Camera dei Deputati')
   # #fig.show()
   # #labels= dataOutput['Partito']
#
   # ax2 = plt.subplot(1,3,3, aspect='auto') #1 row, 2 colonne
   # plt.axis('off')
   # tbl = table(ax2, dataOutput, loc='center')
   # tbl.auto_set_font_size(True)
   # tbl.set_fontsize(100)
   # tbl.scale(1.7, 1.7)
   # plt.show()




    fig, ax = plt.subplots(figsize=(15, 9), subplot_kw=dict(aspect="equal"))

    recipe = dataOutput['Partito']

    data = dataOutput['Seggi']
    partiti = dataOutput['Partito']


    frame = []
    exp = 0.01
    for index in range(len(dataOutput)):
        frame.append(exp)
        exp *= 1.4




    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%\n({:d} seats)".format(pct, absolute)


    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                      textprops=dict(color="black"), explode = frame)

    ax.legend(wedges, partiti,
              title="Partito",
              loc="upper left",
              bbox_to_anchor=(1.01, 0.08, 0.5, 1))

    plt.setp(autotexts, size=4, weight="bold")

    ax.set_title("Distribuzione Nazionale Camera dei Deputati 2013", loc='left')

    plt.show()

  

    return 0