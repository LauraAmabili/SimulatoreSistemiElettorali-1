Candidates are irrelevant for most of the process yet essential for the fine details of the 
simulation. They are identified by a unique string which may or may not contain spaces. As in the 
geographical divisions 
the string will
  be of the form: `string_id` with the `_id` being ignored when it comes to printing the results

The Candidate object needs to fulfill three functions:
1. Presenting a record based on the lane being executed (which defaults to None if the candidate is 
not part of the lane at all)
2. Receiving a proposal by a lane (return value true if the candidate is viable false if not viable, 
so the caller knows to take actions)
3. Picking one of multiple proposals and forwarding the others to the next viable candidate

In particular point 3 is going to rely on a synchronized (thread safe) object being provided with 
the rest of the candidacy in point 2. When the function involved in point 3 is called the object 
will follow these steps:
1. Applying a provided criteria it will accept a candidacy, adding itself to the appropriate lane 
and removing itself from the list of viable candidates. It will also activate an internal flag that 
makes all call to function (1) return None and all calls to function (2) will cause it to reject the 
proposal (that is return False)
2. It will iterate over the refused proposals calling the given function (this call will need to be 
thread safe since the object might be shared by multiple candidates)

# Candidate ordering generation

At the end of a lane the process will have selected a certain amount of Political Entities
