import src.GlobalVars


def parse_columns(cols):
    """
    Parses columns and rename, it receives either a string of the form:
    > name (-> rename)?

    or a list of such strings

    It returns a list and a dictionary, the list is an ordered list of 'name',
    the dictionary is, for each entry with a 'rename', a mapping: 'name':'rename'
    """
    if type(cols) == list:
        lista = map(parse_columns, cols)
        l_f = []
        d_f = {}
        for i in lista:
            l_f.extend(i[0])
            d_f.update(i[1])
        return l_f, d_f
    cols = cols.split('->')
    r = cols[0].strip()
    if len(cols) > 1:
        return [r], {r: cols[1].strip()}
    else:
        return [r], {}


def transform_column(col, tipo):
    def tr(name):
        return src.GlobalVars.Hub.get_instance(tipo, name)

    return col.map(transform_column)


def parse_column_selector_compare(*, column_val=None, column=None, logic="absolute", criteria, target):
    """
    Returns a function that takes in the local, a dataframe and returns the slice of the dataframe respecting the
    criteria
    """
    if column is None:
        column = column_val
        if column_val is None:
            raise TypeError("Either column_val or column must be valid")

    fun_comp = None
    if criteria == 'eq':
        fun_comp = lambda x: x == target
    elif criteria == 'lt':
        fun_comp = lambda x: x < target
    elif criteria == 'gt':
        fun_comp = lambda x: x > target

    if logic == "absolute":
        def filter_absolute(locs, df):
            filt = df.apply(lambda x: fun_comp(x[column]), axis=1)
            return df[filt]

        return filter_absolute
    elif logic == "relative":
        def filter_relative(locs, df):
            total_v = df[column].sum()
            filt = df.apply(lambda x: fun_comp(x[column] / total_v), axis=1)
            return df[filt]

        return filter_relative


def parse_column_selector_take(*, column_val=None, column=None, order, take):
    """
    Returns a function taking local variables, a dataframe and returning a slice of the dataframe
    """
    if column is None:
        column = column_val
        if column_val is None:
            raise TypeError("Either column_val or column must be valid")

    if order == "decreasing":
        ascending: bool = False
    else:
        ascending: bool = True

    def take_rows(locs, df):
        return df.sort_values(column, ascending=ascending).iloc[:take]

    return take_rows
