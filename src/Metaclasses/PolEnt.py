from src import GlobalVars


class PolEnt(type):
    """
    PolEnt aggiunge la classe come subclass di "PolEnt", inoltre
    """
    def __new__(mcs, *args, sub_of=None, **kwargs):
        """
        sub_of: lista di stringhe, ogni stringa indica un parametro di init,
        """

        GlobalVars.Hub.register_subclass(args[0], 'PolEnt')

        if sub_of is not None:
            o_init = args[2].get('__init__', lambda *a, **k: None)

            def __init__(self, name, **k):
                for i in sub_of:
                    v = k.get(i, None)
                    setattr(self, i, v)
                    if v is not None:
                        GlobalVars.Hub.add_political_sub(name, v, args[0])

                return o_init(self, name, **k)
            args[2]['__init__'] = __init__

        return super().__new__(mcs, *args, **kwargs)

    @classmethod
    def parse_conf(mcs, conf):
        return conf
