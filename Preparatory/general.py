import inspect, copy
def deepcopyDecorator(pos_to_drop=0, *kw_to_drop):
    """
    The decorator it creates deepcopies all the parametes except the firs 'pos_to_drop' ones and
    the keyword parameters with key in 'kw_to_drop'
    """

    def deepcopyIntermediate(func):
        """
        Takes the function and returns a function with the same signature but deepcopied args
        """
        sig = inspect.signature(func)
        pars = list(sig.parameters)
        kws_not_copy = copy.deepcopy(list(kw_to_drop))

        for i in range(pos_to_drop):
            kws_not_copy.append(pars[i])

        def f(*args, **kwargs):
            argsNew = args[:pos_to_drop] + copy.deepcopy(args[pos_to_drop:])
            kwargsNew = dict()
            for k,v in kwargs.items():
                if k not in kws_not_copy:
                    v = copy.deepcopy(v)
                kwargsNew[k]=v

            return func(*argsNew, **kwargsNew)

        f.__signature__=sig
        f.__name__ = func.__name__
        return f
    return deepcopyIntermediate
