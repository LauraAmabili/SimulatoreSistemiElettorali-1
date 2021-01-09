import pandas as pd
import src.GlobalVars as gv

pd.options.mode.chained_assignment = None


def correct_porcellum(distretto, distribuzione_ideale, distribuzione_raccolta,
                    info_locali, *info_comuni):
    
    #print("---> CORRECT PORCELLUM <---")

    # distribuzione_raccolta è un dizionario che contiene un distribuzione dei
    # seggi suddivisa però per circoscrizione
    #
    # prende la distribuzione passata
    # con i dati europei la prima distribuzione passata sarà quella generale
    # in cui ogni partito avrà il numero totale di seggi che gli vengono assegnati
    #
    #                        Partito     Seggi
    #       8   LEGA SALVINI PREMIER     30
    #       12   PARTITO DEMOCRATICO     20
    #       6      FRATELLI D'ITALIA      5
    #       4           FORZA ITALIA      7
    #       9     MOVIMENTO 5 STELLE     14 
    #
    # #
    ideal = distribuzione_ideale

    actual_distr = {}
    resti = {}
    
    for k, v in distribuzione_raccolta.items() :

        for _, r in v.iterrows():

            party = r['Partito'] # prendo la lista di questa riga
            o_segg = actual_distr.get(party, 0) # prendo il numero di seggi di questo partito
                                                # se non è presente di default è 0

            actual_distr[party] = r['Seggi'] + o_segg # aggiungo il numero di seggi al partito

            o_resti = resti.get(party, {}) # prendo il numero di resti del partito
                                           # se non è presente di defaul ho dizionario vuoto

            o_resti[k] = info_locali[k][party]['Resto'] # prendo il resto del partito in questa circoscrizione
            resti[party] = o_resti # setto in un dizionario locale il resto
    
    # copia distribuzione_raccolta in df_r
    df_r = {k: v.set_index('Partito') for k, v in distribuzione_raccolta.items()}

    for _, r in ideal.iterrows():

        p = r['Eleggibile']
        s = r['Seggi']

        # conta la differenza di seggi tra la distribuzione ideale
        # (ovvero quella con il numero di seggi totali)
        # rispetto alla distribuzione attuale
        # (ovvero quella con il numero di seggi divisi per circoscrizione)
        diff = int(s - actual_distr.get(p,0))

        # se non ho differenza continua
        if diff == 0:
            continue

        # ora ordina i partiti per il valore del resto con il piu alto per primo
        #
        # ok ruffati, ma come lo sai in che circoscrizione lo devi aggiungere ?
        # te lo dicono per messaggio segreto ? mazzette ?
        # so in che circoscrizioni devo aggiungere
        #
        # in pratica questa è una lista di circoscrizioni con rispettivi resti in cui
        # si dovranno aggiungere i seggi
        # in qualche modo questa funzione lo fa
        #
        # credo che prenda l'intera lista e poi tenga solamente le prime n (n = diff) circoscrizoni
        # con resto piu alto
        resti_p = sorted(list(resti[p].items()), key=lambda x: x[1], reverse=True)[:diff]
        
        # ora assegno i seggi mancanti ai pariti
        for distr, _ in resti_p:
            if p not in df_r[distr].index:
                df_r[distr].loc[p, 'Seggi'] = 0
            df_r[distr].loc[p,'Seggi'] += 1

    ret = {k: v.reset_index() for k, v in df_r.items()}, {},{}

    #print("RET")
    #print(ret)
    
    # restituisco la nuova distribuzione
    return ret


def distrib_porcellum(*a, data, seats, df_partiti_filtrato, df_partiti_regioni, **kwargs):
    print("\n---> TROVO LA DISTRIBUZIONE DEI SEGGI CON IL PORCELLUM <---\n")

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
    if df_eleggibili.iloc[0, df_eleggibili.columns.get_loc('Seats')] < 340 :
        #print("la maggioranza non ha 340 seggi")

        df_eleggibili.iloc[0, df_eleggibili.columns.get_loc('Seats')] = 340

        # Q è la somma di tutti i voti diviso per il numero di seggi generali
        #data2 = data.copy()
        df_eleggibili_2 = df_eleggibili.iloc[1:]

        remainingSeats = seats - 340
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

    print('DISTRIBUZIONE FINALE CON PORCELLUM')
    print(df_eleggibili)


    df_final_distribution = dividi_per_partiti(df_eleggibili, df_partiti, df_coalizioni)
    
    print('DISTRIBUZIONE FINALE CON PARTITI')
    print(df_final_distribution)

    return df_final_distribution


def dividi_per_partiti(df_eleggibili, df_partiti, df_coalizioni):

    print("\n---> SUDDIVIDO I SEGGI DELLE COALIZIONI TRA I PARTITI <---\n")
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
            frame.append(df_eleggibili[df_eleggibili['Eleggibile'] == row_eleggibili['Eleggibile']])
    
    # END-FOR
    df_distribuzione_finale = pd.concat(frame)

    df_distribuzione_finale = df_distribuzione_finale.drop(['Remainder', 'RemainderUsed'], axis=1)

    return df_distribuzione_finale


def divisione_circoscrizionale_seggi(*, information, distribution, district_votes, seggi, **kwargs):

    #print("ESEGUO divisione_circoscrizionale_seggi")

    info = information[1]

    voti_circoscrizione = district_votes.set_index('Partito')['Voti']

    risultato = []
    
    for index, row in distribution.iterrows():

        partito = row['Eleggibile']
        numero_seggi = row['Seggi']
        voti_partito = voti_circoscrizione.get(partito, 0)
        
        voti_nazionali_partito = info[partito]['Voti']
        
        if numero_seggi == 0:
            continue

        q = voti_nazionali_partito / numero_seggi

        seggi_assegnati, resto = divmod(voti_partito, q)

        risultato.append(pd.Series({'Partito': partito, 'Seggi': seggi_assegnati, 'Resto': resto, 'Voti': voti_partito}))


    ret = pd.concat(risultato, axis=1).T

    return ret


def printing_visuals(lista) :



    lista_circoscrizioni = [i[0] for i in lista]
    general_dict = dict.fromkeys(lista_circoscrizioni, {}) 

    for elem in lista:
        
        elem_dict = {}

        circoscrizione = elem[0]
        nome_lane = elem[1]
        nome_partito = elem[2]
        numero_seggi = elem[3]

        general_dict[circoscrizione.name][nome_partito] = numero_seggi

    return lista_circoscrizioni