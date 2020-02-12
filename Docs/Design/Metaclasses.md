# Lane

A lane is the execution "director" for the system, only a single lane will be excuted at any single
time, a lane will start by calling a function on the instances of the lane head. Once the function
returns the results are collected in a set by the hub and iterated over until the actual elected 
results are obtained

Each step of the lane also needs to be able to show how many seats it will assign, this will be set
at the lane tail by default but could be fuzzy or be assigned dynamically at an higher level

Higher levels can deal with it by adding together lower levels. When setting it up I should consider
the following options, because a lane can be used to elect:
+ a fixed number of candidates
+ up to a fixed number of candidates
+ a run-time determined number of candidates
+ up to a run-time determined number

Logs might also be passed along to provide further information, so for instance in the lane for
plurinominal representatives in the Rosatellum the Circoscrizione will pass a dictionary which for
every Coalizione/Partito will give more information

## Lane head
This is where the lane begins, creating the class will register it with the Hub.

It will offer a function which when called will return a **set** of candidates which received an
initial offer for a seat.

It will create the first proposal without any external input and then correct lower level options.

Finally it will pass to every lower level instance the directives it must follow and wait for the
return. The return will be a list of sets which must be merged

## Lane node
A lane node behaves as lane-head except for the transparent propose function which will be called by
the level above and for a function which will behave as start\_lane, but accepting a distribution as
an argument

## Lane tail
This behave as lane node except that instead of calling a sub level it uses the distribution it
uses the information it has received to elect candidates, this will happen by taking the final
dataframe obtained (which will have columns: ["PolEnt", "Seats to assign"]) and on the first column
of each row calling the function provided by the elector metaclass

## Lane direct
This is useful for systems which don't rely on higher levels to decide the representation, these are
systems such as FPTF, multi-member district proportional etc.

It is conceptually the same as a lane having the same class as both Lane-head and Lane-tail

# Superdivision
Defines the name of the subdivisions (as an aggregate) and the Class it is made up of.

For instance in Uninominale will define sezioni as the subsection and Sezione as the class name

It will provide aggregation functions concatenating different call returns applied on the
subsections. This way totals only needs to handle input from functions. This is only going to be a
simple concatenation, which can be handled by an aggregating total

# Totals (data elaboration)
Totals can work in one of different ways:
+ Aggregation, takes a result with duplicate homogeneous records and adds them together, but doesn't
transform in any other way. From many (an arbitrary number) to 1. Ex: 
+ Combination, takes heterogeneous data and combines into one result. From n to 1
+ Transformation, takes a result and transforms into another, from 1 to 1

A combination of these can be achieved by assigning each intermediate step a different value

The default behaviour is to apply filters (as defined in the filter metaclass) to the output of the
function and forward it to different function calls. 

More specifically a call to filter can return:
+ None: the filter needs to be applied downstream, forward it
+ A function that can be applied to a row of the result and gives a Boolean result, don't forward

If a filter needs to change it must be specified in the definition of a totals function

# Elector
Provides a function to elect a number of candidates to the seats in a specific lane in a specific
district (generates the iterator and makes the first n proposals), returns the names of the
propositioned candidates

And a function to represent the candidate options for a specific lane/area

The second function can be used by the first, for instance this way I can handle a candidate having
information both for its role as a loser majoritarian candidate and as a plurinominal candidate

# Candidate
Will receive offers and have to accept them, I have to provide the criteria in which to order each 
lane's offers. It's safe to assume for each lane offers are consistent, so this can be an ordered
list of columns on which to order the offers, the candidate will accept the first and forward the
next ones

# Initializer
Specifies what must be specified in the init function

# Filtering
When totals receives a blocking command it calls on every first column of each row the filter,
providing:
+ The name of the class which is running totals, and its instance name (type and str)  
This way it can use the unfiltered result if needed
+ The name of the total being executed (party, coalition, candidate\_raw ...)
+ The row itself

The filter returns true if the row is to be used

Two types of filter:

+ In the german system I use a filter that checks if the personal candidate has been elected, in
which case depending on its party of origin I can count or ignore the second vote
+ In the rosatellum system and other proportionals I use it to check for the electoral threshold

# Receive data
Can be used to collect logs or receive data, can be set to incremental or overwriting (for
instance the same data will not get repeated

You must define the shape of the data, a name and the nature of the data (overwrite/accumulate)

Optionally allow the value to be retrieved as a function call instead of a parameter

# Logger
**Needs to follow totals in the order**

Wraps around a function and has a side effect before returning the result. Must specify which
fucntion to wrap and where the message must be sent

# Data source
(obsolete, replaced by receive data and a totals)

# Main

Needs to do cleanup
