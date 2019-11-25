# The hub
The hub is the center of the simulator instance, it allows classes to be defined in whichever 
order is most comfortable to the user by abstracting away the instance retrieval

Classes can now be retrieved just by knowing their literal name, `Hub.getClass('name')`, instances
can be accessed by knowing their class and name `Hub.getInstance('class', 'instance')` or 
`Hub.getInstances('Class')`.

**Goal: keep track of which classes are under which other classes in the subsections**

How: the subsection metaclass will call: `Hub.addSubs(classe, *subclasses)`

**Goal: Allow a function to find, given an instance of a GeoDiv, the superdivision, belonging to a
given class, of the instance**, this could be used for instance when I want to check if a class
passes the minimum requirements.

How: classes that are derived through Subsection have the function `isAncestorOf(instance)`, this
function just retrieves all instancess of the target class and filters them based on the above 
function

**Goal: abstract away class derivations** so as to allow the grouping of different classes under
the same name, could be useful for parties for instance, since some might have different 
qualification requirements but still need to be treated as the same when looking instances up

How: Allow a field in the class definition structure that when parsed will call:
`Hub.createSubClass(superclass, subclass)`, instance retrieval (but not class retrieval) functions
will check if the required class has any subclasses and integrate it
