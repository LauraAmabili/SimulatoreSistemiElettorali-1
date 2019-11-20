# Notes:

## Critical

##### Call by reference shenanigans
When generating a function the parameter is passed by reference, so if I generate a function which
uses a dict and then change the dict the function behaviour will be affected

It should be mitigated if I reset the values, or pass hard copies each time


# Todo:

## Proof of concepts

Put together in a single structure all proof of concepts scattered across the project
+ Adding functions via metaclasses
+ Generating a closed function from given attributes
+ Chaining multiple function calls
