from src import GlobalVars
from src import Commons
commons = Commons

class party(type):
    

    def __new__(mcs, *args, **kwargs):
        #print("ARGS : ", args)
        o_init = args[2].get('__init__', lambda *s, **k: None)

        def __init__(self, *a, **kwargs):
            self.percNazione = 0.
            self.percRegione = 0.
            self.votiPartito = 0
            return o_init(self, *a, **kwargs)

        args[2]['__init__'] = __init__
        return super().__new__(mcs, *args, **kwargs)


    @classmethod
    def parse_conf(mcs, conf):
        return conf