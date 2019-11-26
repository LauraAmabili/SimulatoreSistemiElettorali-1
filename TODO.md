# Todo for the project

## Missing feature
+ adding an attribute to a class (similar to data\_source) like for providing lists

## Essential

+ When calling a totals function allow to overwrite the "sbarramento" parameter (as in providing
a static one instead of just relaying, I anyway need that)
+ Consistent method to generate candidate list
+ Method to see who has been elected in a given geographical area by a given party/coalition

## Priority

+ Thread safe iterator for the candidate list

## Bug fixes:
+ Make data sources convert columns which should be onbjects into actual objects (everything else
assumes they are object

The combination as defined currently in conventions.md doesn't work with multiple column 
aggregation and scalars

## Almost ready

+ Apply a function on a column 
+ Merging different data sources through a function

## Todo for examples

+ Function to adjust seats between "circoscrizioni" et simile
