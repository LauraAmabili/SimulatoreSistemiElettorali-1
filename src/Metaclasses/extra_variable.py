# -*- coding: utf8 -*-
class extra_variable(type):
    def __new__(cls, *args, **kwargs):
        # Modifica l'init della classe creata
        pass

    @staticmethod
    def parse(dizionario):
        """
        Ricevo un dizionario stringa:stringa
        La stringa chiave è il nome della variabile, la stringa value è la classe.
        Aggiungere ad init il parametro e un type_check

        :param dizionario:
        :return:
        """