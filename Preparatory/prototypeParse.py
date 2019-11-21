import copy


def tempColName(columns, first_choice):
    if first_choice not in columns:
        return first_choice

    c = 1
    while f"{first_choice}_{c}" in columns:
        c+=1
    return f"{first_choice}_{c}"

def deepCopyArgs(*args):
    def deepCopyArgasNoParam(func):

        def f(*args, **kwargs):
            args = copy.deepcopy(args)
            kwargs = copy.deepcopy(kwargs)
        return func(*args, **kwargs)
    return f

@deepCopyArgs TODO: implement excluding arguments
def sub_map_total(hubRef, subListName, totalsId):
    def returned(self, sbarramento=False):
        iterator = map(lambda s: hubRef.getInstance(self.tipi_sub[subListName],s)
                                    .totals(totalsId, sbarramento), getattr(self, subListName))
        return pd.concat(iterator, ignore_index=True).copy(deep=True)

    return (returned, f"map_{subListName}_{totalsId}")

@deepCopyArgs
def totalsFromSubs(subList, totalsId, aggrKey, aggrDict, renameDicts=[], filterDict={}):
    """
    subList :: String -> The name of the subsections I'm querying
    totalsId :: String -> The id of the totals function to be called on the subList
    aggrKey :: String | Tuple[String] -> the keys to aggregate on
    aggrDict :: Dict[String, PandasAcceptable] -> The rules for the aggregation
    renameDicts :: List[Dict[String, String]] -> The first element renames the concatenated dataframe
                                                before applying the aggregation. The second renames
                                                the aggregated dataframe before returning it
    filterDict :: Dict[String, Filter] -> For the "sbarramento". If sbarramento is a key then 
                                        prior to returning it I filter the dataframe with the 
                                        appropriate Filter
    """
    renameDicts.extend([{},{}])

    def totals_gen_from_sub(self, sbarramento=False):
        sub = getattr(self, subList)
        tipo = self.tipi_sub[subList]
        data = getattr(self, f"map_{subList}_{totalsId}")(sbarramento)
        data.rename(columns=renameDicts[0], inplace=True)
        groups = data.groupby(aggrKey)
        res = groups.agg(aggrDict)
        res.rename(columns=renameDicts[1],inplace=True)
        if sbarramento in filterDict.keys():
            qualified = tempColName(res.columns, "qualified")
            res[qualified] = res.apply(filterDict[sbarramento], axis=1)
            res = res[res[qualified]==True]
            del res[qualified]
            res.reset_index(drop=True, inplace=True)

        return res
    return totals_gen_from_sub


