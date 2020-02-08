

class logger(type):
    def __new__(mcs, *args, **kwargs):
        o_log = args[2].get('log', lambda *a, **k: None)
        o_init = args[2].get('__init__', lambda *a, **k: None)

        def log(self, district, lane_name, **info):
            print("Logging for ", district, " in ", lane_name, ": ", info)
            self.logs[lane_name][district] = info

        def __init__(self, *a, **k):
            self.logs = {}
            return o_init(self, *a, **k)

        args[2]['log'] = log
        args[2]['__init__'] = __init__
        return super().__new__(mcs, *args, **kwargs)