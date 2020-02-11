from copy import deepcopy
import src.utils
from src import Commons
commons = Commons


def function_arg_parser(source_parser, name, args=None,
                        kwargs=None, **other_confs):
    # print("Parsing fun: ", name, args, kwargs, other_confs)
    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}
    """
    Parses the function, returns a function that requires:
    + local namespace
    + *args
    + **kwargs

    And returns the value
    """
    fun = deepcopy(name)
    args = deepcopy(args)
    kwargs = deepcopy(kwargs)

    args = [source_parser(i, True) for i in args]
    kwargs = {k: source_parser(v, True) for k, v in kwargs.items()}

    def return_fun(local, *n_args, **n_kwargs):
        # print("ret_fun_parse:", args)
        eff_args = [i(local, *n_args, **n_kwargs) for i in args]
        eff_kwargs = {k: v(local, *n_args, **n_kwargs) for k, v in kwargs.items()}

        eff_args = eff_args + list(n_args)
        eff_kwargs.update(n_kwargs)

        globs = globals()
        globs['Commons'] = src.Commons
        globs['commons'] = src.Commons
        # print("Locals prima di cercare la funzione: ", local)
        # print("Cerco funzione: ", fun)
        f = eval(fun, globs, local)
        # print(f)
        return f(*eff_args, **eff_kwargs)
    return return_fun


def attribute_arg_parser(source_parser, name, **other_confs):
    """
    Returns a function accepting a namespace, *args and **kwargs, ignores the ?args and
    returns the value
    """
    def return_fun(local, *args, **kwargs):
        # print("Locals prima di trovare l'attributo: ", local)
        return eval(name, globals(), local)

    return return_fun


def kwarg_arg_parser(source_parser, name, dic_name="kwargs", **other_confs):
    def return_fun(local, *args, **kwargs):
        return local['kwargs'][name]
    return return_fun


def source_parse(configuration, in_source=False):
    # print("Parsing conf: ", configuration)
    if not in_source:
        if type(configuration) == list:
            return [source_parse(i, in_source) for i in configuration]

        if type(configuration) != dict:
            return configuration

        # print("prova, ", configuration.keys())
        return {k: source_parse(v, k=='source') for k, v in configuration.items()}

    # print("In source")

    if type(configuration) != dict:
        def simple_res(*args, **kwargs):
            return configuration
        return simple_res

    if 'source' in configuration:
        return source_parse(configuration['source'], in_source)

    t = configuration['type']
    if t == 'fun':
        parsed = function_arg_parser(source_parse, **configuration)
    elif t == 'att':
        parsed = attribute_arg_parser(source_parse, **configuration)
    elif t == 'kwarg':
        parsed = kwarg_arg_parser(source_parse, **configuration)
    else:
        raise AttributeError('Neither function nor attribute')

    columns = configuration.get('columns', [])
    columns, rename = src.utils.parse_columns(columns)
    rename.update(configuration.get('rename', {}))

    store_action = configuration.get('store', None)
    options = configuration.get('options', [])

    def function_returned(local, *args, **kwargs):
        if 'NoForward' in options:
            args = []
            kwargs = {}
        r = parsed(local, *args, **kwargs)

        if len(columns) > 0:
            r = r[columns]

        if len(rename.keys()) > 0:
            r = r.rename(columns=rename)

        if store_action is None:
            pass
        elif store_action[0] == '#':
            setattr(local['self'], store_action[1:], r)
        elif store_action[0] == '$':
            d, k = tuple(store_action[1:].split('.')[:2])
            local[d][k] = r
        else:
            local[store_action] = r
        return r

    return function_returned
