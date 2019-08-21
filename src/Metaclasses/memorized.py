# -*- coding: utf-8 -*-
class memorized(type):
    def __new__(cls, *args, **kwargs):
        # Modifica il new, è importante il "nome" kwarg

        pass

    @staticmethod
    def parse(lista):
        """
        Keys:
            + variable, the name of the attribute of Hub in which to save the elements
        :param lista:
        :return:
        """