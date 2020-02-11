from src import GlobalVars


class subclass(type):
    def __new__(mcs, *args, subclass, **kwargs):
        for i in subclass:
            GlobalVars.Hub.register_subclass(args[0], i)
        return super().__new__(mcs, *args, **kwargs)