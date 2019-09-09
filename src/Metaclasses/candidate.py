"""
TODO: have the means to receive multiple offers (asynchronously), accept a single offer and propose to the second choice
candidates for unaccepted choices
"""


class Candidate(type):
    # Provide: pick_spot(), returns a string
    def __new__(mcs, candidate, *args, **kwargs):
        # -------------------- pick_spot(): return
        def pick_spot(self):
            # access self.proposals, self.onAccept



        # -------------------- get_proposal(**kwargs) -> Bool:
        def get_prop(self, *, nextChoiceIter, onAccept, **kwargs):
            """

            :param self:
            :param nextChoiceIter:
            :param onAccept: void -> String
            :param kwargs:
            :return:
            """
            pass

        pass
