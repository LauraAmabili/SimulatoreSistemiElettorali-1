from src import GlobalVars
"""
TODO: have the means to receive multiple offers (asynchronously), accept a single offer and propose to the second choice
candidates for unaccepted choices
"""


class Candidate(type):
    # Provide: pick_spot(), returns a string
    def __new__(mcs, *args, candidate, **kwargs):
        _
        o_init = args[2].get('__init__', lambda *s, **k: None)

        def __init__(self, *args_in, **kwargs_in):
            self.proposals = []
            self.elected = False
            return o_init(self, *args_in, **kwargs_in)

        def propose(self, lane, district, iterator):
            if self.elected:
                return next(iterator).propose(lane, district, iterator)

            self.proposals.append((lane, district, iterator))
            return self.name

        def decide(self, lane):
            # TODO: Decide how to describe the logic
            pass

        # TODO: add functions to arguments and call super().__new__(...)
        pass
