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
# TODO: the lane process starting in the lane_head should return a list of strings where the strings are the identifiers
    # of the candidates which received a proposal by the lane
    # the lane should also, as an intentional side effect, provide each proposed candidate with the information it needs
    # to make a choice and to pass down the choice


class lane_head(type):
    """
    La configurazione di lane_head DEVE indicare un numero prioritario, le lane saranno eseguite in sequenza dando
    priorità a numeri più bassi

    Il punto di partenza della Lane, per esempio nazione. Salvato in hub
    Sa solo correggere le proposte ottenute e calcolare un exact_value
    """
    def __new__(cls, *args, lane_head, **kwargs):

        # Funzione start_lane('lane')

        # Funzione is_lane_endpoint('lane') (controlla che la funzione non esista già, nel caso decorala e basta)

        # Funzione get_lane_sub('lane')

        # funzione correggi('lane', **kwargs)

        # aggiungi funzione a args[2] (dict)
        super().__new__(cls, *args, **kwargs)



class lane_middle(type):
    """
    Un nodo intermedio, propone al nodo superiore, riceve la correzione e corregge i nodi inferiori
    """

    # Funzione is_lane_endpoint('lane') (controlla che la funzione non esista già, nel caso decorala e basta)

    # Funzione get_lane_sub('lane')

    # Funzione proponi('lane', **kwargs)

    # Funzione correggi('lane', **kwargs)


class lane_bottom(type):
    """
    Il nodo che riceve le informazioni dai punti precedenti ed elegge dei rappresentanti

    Ha la funzione per eleggere, per fornire una proposta e per ricevere il valore corretto
    """
    # funzione is_end_of_lane('lane') true

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