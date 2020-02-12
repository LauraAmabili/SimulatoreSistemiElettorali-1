import pandas as pd


def assign_local_seats(*, information, distribution, district_votes, **kwargs):
    info = information[1]
    votes_s = district_votes.set_index('Lista')['Voti']
    res = []
    for _, i in distribution.iterrows():
        p = i['Lista']
        seats = i['Seggi']
        votes_n = info[p]['Voti']
        q = votes_n/seats
        votes_l = votes_s.get(p, 0)
        s, rem = divmod(votes_l, q)
        res.append(pd.Series({'Lista': p, 'Seggi': s, 'Resto': rem}))

    return pd.concat(res)