# Seats, candidates and parties

Seats are the targets of the election procedure, and they can only be filled by individuals, not
directly by parties.

Therefore every system must have a candidate object to represent such an entity.

While this is sufficient for plurality wins or runoff voting systems such as FPTP or STV this is not
sufficient for managing proportional representation systems which rely on the structure provided by
parties or even coalitions.

In these cases a seat that is in theory assigned to a party might in fact be assigned to a coalition
partner or to a candidate from the same partner that didn't stand for election in the given
constituency.

Moreover in these systems a minimum amount of national votes is often required to be considered for
seat redistribution.

From this we know that we have different levels of political entities, Candidate, Party, Coalition;
and that for each of these we will need to be able to access the amounts of votes each political
entity won at different levels.

So the methods for all political entities must be:
+ totals :: GeoEnt -> Int
+ passedBlock :: String -> GeoEnt -> Bool
+

# Lane endpoints
Lanes end in a GeoEnt, the lane endpoint will have to take a decision based on the result of a
total function application.

**Convention**: the first column must be the one to which distribute seats

So the endpoint will decide to associate a certain row with a number of seats and other arguments
and will call the `.elect(lane, self, seats, **args)` on the element of the first column.

If the element is a 


-----------

How to handle the open list proportional?

Option 1:
+ The party list determines who gets more votes and grants them the votes. I would have to handle
the polents as a sort of dataframe inside of them

Option 2:
+ Allow the sorting to happen on the geographical level, how? I'd need to call them by grouping

Which is less bothering?

**Decision:**

Go with option 1, cleaner, you can implement some of the logic in the party structure and it's
trivial for a party to retrieve its totals

-----------

So it will go like this:

1. The lanes ends with the leaf knowing that it must give some amount of seats to a certain polent
etc
2. The leaf calls elect on the political entity providing the number to elect, the lane which
elected them, itself and then the kwargs passed from upstream which might be needed to make a
decision
3. The political entity will gather the information it needs and then call elect as needed
	+ It will also create the iterator, trivial to do in this case
4. I aggregate all the elected candidates and go on as planned

**Problem**: I might need to wait for all leaves to run "elect" before I can return the list of 
candidates.

**Possible Solution**: Return an iterator and make sure they are only called after every iterator
has been returned































