def hondt(df, seats):
    df = df.copy()
    q = df['Votes'].sum()/seats
    df['Seats'] = df['Votes'] // q
    df['Seats'] = df['Seats'].astype("int")
    df['Remainder'] = df['Votes']/q - df['Seats']
    df['RemainderUsed'] = False
    r = seats - df['Seats'].sum()
    df.sort_values('Remainder', ascending=False, inplace=True)
    df.iloc[:r, df.columns.get_loc('RemainderUsed')] = True
    df.iloc[:r, df.columns.get_loc('Seats')] += 1
    return df
