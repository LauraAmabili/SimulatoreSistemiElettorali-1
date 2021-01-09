from src import GlobalVars


class cleanup(type):
    def __new__(mcs, *args, **kwargs):
        typ = args[0]
        o_init = args[2].get('__init__', lambda *x, **k: None)

        def __init__(self, name, *args, **kwargs):
            #print("Cleanup init", self, name, args)
            self.type = typ
            self.name = name
            GlobalVars.Hub.add_instance(typ, name, self)
            return o_init(self, name, *args, **kwargs)
        args[2]['__init__'] = __init__
        #print("Cleanup:", args, kwargs)
        return super().__new__(mcs, *args)
