import pandas as pd


def assign_local_seats(*, information, distribution, district_votes, **kwargs):
    print(information, distribution, district_votes)
    info = information[1]
    votes_s = district_votes.set_index('Partito')['Voti']
    res = []
    for _, i in distribution.iterrows():
        p = i['Partito']
        seats = i['Seggi']
        votes_n = info[p]['Voti']
        if seats == 0:
            continue
        q = votes_n / seats
        votes_l = votes_s.get(p, 0)
        s, rem = divmod(votes_l, q)
        res.append(pd.Series({'Lista': p, 'Seggi': s, 'Resto': rem}))

    print(res)
    ret = pd.concat(res, axis=1).T
    print(ret)
    return ret


def correct_europee(distretto, distribuzione_ideale, distribuzione_raccolta,
                    info_locali, *info_comuni):

    ideal = distribuzione_ideale

    actual_distr = {}
    resti = {}
    for k, v in distribuzione_raccolta.items():
        for _, r in v.iterrows():
            party = r['Lista']
            o_segg = actual_distr.get(party, 0)
            actual_distr[party] = r['Seggi'] + o_segg
            o_resti = resti.get(party, {})
            o_resti[k] = info_locali[k][party]['Resto']
            resti[party] = o_resti
    df_r = {k: v.set_index('Lista') for k, v in distribuzione_raccolta.items()}
    for _, r in ideal.iterrows():
        p = r['Partito']
        s = r['Seggi']
        diff = int(s - actual_distr.get(p,0))
        if diff == 0:
            continue
        resti_p = sorted(list(resti[p].items()), key=lambda x: x[1], reverse=True)[:diff] # so in che circoscrizioni devo aggiungere
        for distr, _ in resti_p:
            if p not in df_r[distr].index:
                df_r[distr].loc[p, 'Seggi'] = 0
            df_r[distr].loc[p,'Seggi'] += 1

    ret = {k: v.reset_index() for k, v in df_r.items()}, {},{}
    return ret


def distrib_europee(*a, data, seats, **kwargs):
    print("Hondt", kwargs, a)
    data = data.copy()
    q = int(data['Votes'].sum() / seats)
    data['Seats'] = data['Votes'] // q
    data['Seats'] = data['Seats'].astype("int")
    data['Remainder'] = data['Votes'] / q - data['Seats']
    data['RemainderUsed'] = False
    r = seats - data['Seats'].sum()
    data.sort_values('Remainder', ascending=False, inplace=True)
    data.iloc[:r, data.columns.get_loc('RemainderUsed')] = True
    data.iloc[:r, data.columns.get_loc('Seats')] += 1
    print("Risultato hondt:", data)
    return data



def printing_visuals(dataset) :

    #printing visuals not defined for europee

    return 0