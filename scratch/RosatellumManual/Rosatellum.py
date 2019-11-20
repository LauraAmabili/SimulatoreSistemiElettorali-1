import pandas as pd

class Hub:
    pass

class Sezione:
    def __init__(self, nome):
        self.nome = nome
        Hub.addInstance("Sezione", nome, self)

    def load_data(self, tipo, dataframe):
        setattr(self, tipo, dataframe)

    def totals(self, tipo, sbarramento=False):
        if tipo == "uninominale":
            return getattr(self, "df_uninominale")
        
        if tipo == "lista":
            return getattr(self, "df_liste")

        return None

def hondt(votes, seats, mapping={''}):
    """
    This function takes a dataframe with two columns, one indicating the recipient of seats,
    the other indicating the weight (votes). It then takes a number of seats to partition and
    a mapping.

    It will return a dataframe with two columns: Recipient, Seats

    The mapping needs the following three keys:
        + "party": the recipient of the seats
        + "votes": the weight
        + "seats": the repartitioned quantity
    """
    pass

class Uninominale:
    def __init__(self, nome, sezioni):
        self.nome = nome
        self.sezioni = sezioni
        self.tipi_sub = {"sezioni":"Sezione"}
        Hub.addInstance("Uninominale", nome, self)

    def sub_map_sezioni_uninominale(sbarramento=False):
        iterator = map(lambda s: Hub.getInstance(self.tipi_sub['sezioni'], s)
                                    .totals("uninominale", sbarramento), sezioni)
        df = pd.concat(iterator, ignore_index=True)
        return df

    def sub_map_sezioni_lista(sbarramento=False):
        iterator = map(lambda s: Hub.getInstance("Sezione", s)
                                    .totals("lista", sbarramento), sezioni)
        df = pd.concat(iterator, ignore_index=True)
        return df

    def totals(self, tipo, sbarramento=False):
        if tipo == "uninominale":
            a = self.sub_map_sezioni_uninominale().groupby("candidato")
            g = a.agg({'voti_cand':'sum'})
            g.rename(columns={'voti_cand':'voti'}, inplace=True)
            return g

        if tipo == "lista_raw":
            a = self.sub_map_sezioni_lista().groupby(("candidato","lista"))
            g = a.agg({'voti_lista':'sum'})
            return g.reset_index(drop=True)

        if tipo == "lista":
            c_votes = self.totals('uninominale').rename(columns={'voti':'tot_coal'})
            l_votes = self.totals('lista_raw')
            args = pd.merge(c_votes, l_votes,on='candidato')
            res_df = args.groupby('candidato').apply(hondt, mapping={...})
            res_df = res_df.reset_index(drop=True)
            return res_df

    def start_lane(self, tipo):
        if tipo == "uninominale":
            return self.elect('uninominale')

    def elect(self, tipo):
        if tipo == 'uninominale':
            ris = self.totals('uninominale')
            seats = 1
            ris = ris.sort_values('voti_cand', ascending=False)
            it = iter(ris.iloc[:, ris.columns.get_loc('candidato')])
            props = set()
            while seats > 0:
                n = next(it)
                r = n.proposeSeat(self, it)
                if r==True:
                    seats-=1
                    props.add(n)
            return props

    def elects_reps(self, lane): # :: String -> Set<(String, String)>
        if lane=='uninominale':
            return set(self.nam)
        

class Plurinominale:





































