# Interfaces
In this document I'll simply list all functions provided by various metaclasses and classes, with
at most a short description

## Hub
The glue holding the system together

+ `getClass(className: str) -> class`: returns the class with the given name, useful for instance 
creation
+ `getInstance(className: str, instanceName: str)`: returns the instance of the given class with
the given identification
+ `getAllInstances(className: str)`: returns a list of all instances of the given class
+ `addSubclass(superclass: str, subclass: str)`: registers that superclass is above the subclass,
might be needed by functions like those determining if a party passed a threshold
+ `addDerivedClass(original: str, derived: str)`: not to be confused with addSubclass (which is
related to geographical relationships) this is about class inheritance, when requesting instances
of the original class all instances of derived classes will also be shown
+ `executeLane(lane: str)`: Starts the lane, this must be outside of the classes because 


## Metaclasses

### Superdivision
Establishing an hierarchy 

+ `getSubOptions()`: Returns a dictionary with keys the variables holding subdivisions and values
their type
+ `getSubs(kind: str)`: returns list of subdivisions from the given variable
+ `containsSub(instance)`
+ `containsSub(className: str, instanceName: str)`: returns true if the given instance is under 
the superdivision at some level
+ `electedInArea(laneType: str)`: returns a series of all those that have been elected in the area
or sub-areas for the given lane

## Political Entity
Parties, Coalitions and Candidates

+ `matches(entity: PolEnt)`: returns true if it matches the given political entity, this is true if
it's the same entity but also if called on a party providing a member of the party or on a coalition
providing a party or member of a party


## Lanes

***IMPORTANT***: the lanes might need to pass some further information along when giving the
constraints, for instance 'Circoscrizione' will pass for each party not only the seats to assign but
also the margin and the unused remainder. This will then be needed by the political entities and 
passed by the leaf
