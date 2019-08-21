# -*- coding: utf-8 -*-
class sbarramento(type):
    def __new__(cls, *args, **kwargs):

        # funzione supera_sbarramento('tipo', subdivision, **kwargs)

        pass

    @staticmethod
    def parse(dizionario):
        """
        Ci possono essere diversi tipi di sbarramento, per ognuno definisco una configurazione nel file
        + query_origin: Il livello sul quale viene calcolato lo sbarramento, in particolare chiamo il partito con la
        chiamata partito.sbarramento("tipo_a", istanza_del_livello) e la funzione di sbarramento opera su istanza del livello

        Problema: aggiungere il riferimento a totals e quali colonne usare

        + criteria: identifica la funzione, può essere una funzione custom (provided) o una funzione di libreria. Il
        parser deve trasformare la descrizione della funzione in una lambda che prende in input un'area geografica e
        restituisce un boolean
        
        :param dizionario:
        :return:
        """