import pandas as pd
import yaml

conf = """
metaclasses:
  - logger # aggiunge automaticamente una funzione log
  - subclass

subclass:
    - PolEnt
"""

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)
metas_p
comb_p = type("combPol", tuple(metas_p), {})


class Partito(metaclass=comb_p, **conf):
    def elect(self, lane, district, seats, **info):
        candidati = src.GlobalVars.Hub.get_political_subs(self, "Candidato", actual=True)
        df_t = []
        for c in candidati:
            df = c.get_log('lista')
            df['Candidato'] = c
            df_t.append(df)

        df = pd.concat(df_t, sort=True)
        ord = df[df['Circoscrizione'] == district.name].sort_values('Voti')
        print(ord)
        it = iter(ord['Candidato'])
        ret =  []
        for i in range(seats):
            c = next(it)
            n = c.propose(lane, district, self, it, **info)
            if n is not None:
                ret.append(n)
        return ret

    def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs):
        if sbarramenti[0] == 'elette':
            print("Filtering elette", total, row, dataframe, district)
            if district.type != 'Nazione':
                return True
            tot_voti = dataframe['Voti'].sum()
            p_voti = row['Voti']
            return p_voti > tot_voti*0.10
        return True
