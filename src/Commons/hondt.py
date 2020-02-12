def hondt(*a, data, seats, **kwargs):
    print("Hondt", kwargs, a)
    data = data.copy()
    q = data['Votes'].sum() / seats
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
