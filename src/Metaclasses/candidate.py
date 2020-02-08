from src import GlobalVars
"""
TODO: have the means to receive multiple offers (asynchronously), accept a single offer and propose to the second choice
candidates for unaccepted choices
"""


class candidate(type):
    def __new__(mcs, *args, candidate, **kwargs):
        o_init = args[2].get('__init__', lambda *s, **k: None)
        belongs = candidate.get('belonging', {})
        def __init__(self, *a, **kwargs):
            self.proposals = []
            self.elected = False

            for name, v in belongs.items():
                setattr(self, name, kwargs[v])

            return o_init(self, *a, **kwargs)

        def propose(self, lane, district, party, iterator, **info):
            if self.elected is not False:
                try:
                    return next(iterator).propose(lane, district, party, iterator, **info)
                except StopIteration:
                    return None

            self.proposals.append((lane, district, party, iterator, info))
            return self.name

        args[2]['pick'] = mcs.parse_pick(**candidate)
        args[2]['__init__'] = __init__
        args[2]['propose'] = propose
        return super().__new__(mcs, *args, **kwargs)

    @classmethod
    def parse_pick(mcs, *, info_vars, criteria, **kwargs):
        if criteria == "first":
            def pick_fun(proposals):
                return proposals[0], proposals[1:]
        elif type(criteria) == list:
            def pick_fun(proposals):
                props = proposals
                for i in criteria:
                    props = sorted(proposals, key=lambda x: x[4][i])
                return props[0], props[1:]
        else:
            pick_fun = eval(criteria)

        def pick(self):
            accepted, passed = pick_fun(self.proposals)
            self.proposals = []
            others = []
            for i in passed:
                l = list(i)
                try:
                    others.append(next(l[3]).propose(*l[:4], **l[4]))
                except StopIteration:
                    pass

            ret = {'info': list(accepted)[:3],
                   'name': self.name}
            for i in info_vars:
                ret[i] = getattr(self, i, "")

            return ret, others
        return pick
