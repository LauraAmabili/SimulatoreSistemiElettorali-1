"""
This is a proof of concept for a drill down/roll up system aimed at handling votes which cumulate on
two axis:
    + Geographical
    + Political

This mechanism is at the core of every decision in an electoral system

Requirements:
    1. Structure must be flexible, a party might not be in a coalition and a coalition might not 
        qualify, requiring its parties to be handled individually
    2. Leave the decision making at the lower level. Implement qualification criteria as a function 
        of the political entity
    3. Decisions must follow, not precede
    4. I know what I'm looking for, not how to get it, declarative programming

Example:

    Since coalitions depend on the parties and are optional I don't want to be asking the coalition
    for how many votes it got and if it passed. I want to map over the parties and parties in the 
    same, successful, coalition will return the same value.

Naming standard:
    + PolEnt = Candidate | Party | Coalition
    + GeoEnt = District | Super GeoEnt
    + Type = String

Call convention:
    + GeoEnt.getVotes(Type [, PolEnt])
    + PolEnt.getVotes(Type [, GeoEnt])

    Both will reduce to GeoEnt method since a geographical entity is more stable than a political

We can assume there exists a global list of political entities and a global reference to the 
geographical root

The political entities one is a dictionary with keys the type of the get request. So, for instance:
    + coaliz: [Partito1, Partito2, Part3 ..., Coal 1, ..]
    + uninom: [...]
    + lista: 
    Depending on the instance parties might also 

"""

class Criteria:
    def __call__(self, polEnt, geoEnt=Null):
        """
        This defines the criteria class of an entity, 
        """

class PolEnt:
    """
    Attributes:
        + totals_dict: Dictionary where the keys are the supported operations and the values are the
                        objects actually implementing the operation
    """
    def __init__(self):
        self.totals_dict = dict()

    def getVotes(tp, geoEnt=None):
        pass

    def inGeoEnt(geoEnt):
        pass

class GeoEnt:
    def getVotes(tp, polEnt=None):
        """
        If called without a polEnt it's supposed to return the total of votes cast in a region
        """
        pass

#o--------------------

class Party(PolEnt):
    def __init__(self, nome, id_coalizione="")
        self.nome = nome
        self.coalizione = coalizione

        if self.coalizione is "":
            self.totals_dict["pluri"] = self
        else:
            self.totals_dict["pluri"] = 

































