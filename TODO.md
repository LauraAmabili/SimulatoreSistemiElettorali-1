# Todo for the project

## Missing feature
+ adding an attribute to a class (similar to data\_source) like for providing lists
+ The lanes metaclass in addition to being included in the other class configurations needs its
own configuration to tell the Hub the order of execution and a global ordering
+ for the lanes part I need to gather all the lanes and determine an order before starting the
process. Two options:
   1. The lane head will tell which lanes have to be present before this one starts
   2. I write an extra file with this information

+ str on a class returns the name
+ Totals accepting function arguments, forwarding the 

## Essential

+ When calling a totals function allow to overwrite the "sbarramento" parameter (as in providing
a static one instead of just relaying, I anyway need that)
+ Consistent method to generate candidate list
+ Method to see who has been elected in a given geographical area by a given party/coalition

## Priority

+ Thread safe iterator for the candidate list

## Is it a problem?
+ Forwarding the candidate currently passes only the information that was given to the first 
candidate, could I need to give different information? Kinda

## Bug fixes:

+ Make data sources convert columns which should be onbjects into actual objects (everything else
assumes they are object
   + Do they?

The combination as defined currently in conventions.md doesn't work with multiple column 
aggregation and scalars

## Almost ready

+ Apply a function on a column 
+ Merging different data sources through a function

## Todo for examples

+ Function to adjust seats between "circoscrizioni" et simile
