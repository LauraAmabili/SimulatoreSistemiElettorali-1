# Class configuration
This will be a yaml file consisting of (when loaded into python) a dictionary.

Each key represents a class that is to be created and will have its own subdictionary, the keys of which represent
 the metaclasses to be used in the creation of the class.

The loader will therefore first create an Hub object, then iterate over the keys of the main dictionary. For each
 element it will iterate over the metaclasses, loading each metaclass in the basis list and keeping the arguments in
  the dictionary.

Finally it will create the combined metaclass (by adding in the last position a metaclass to catch any unconsumed
 keyword arguments) and use it to create the class, providing the creation process with:
+ The Hub object
+ The dictionary of arguments

Each metaclass will then consume its own parameters

# Class instantiation
This file will provide the information to each instance creation. Will also be a YAML file in the form of a list of
 elements, each element will specify the class to be used and a dictionary with the parameters

# Data providing
These files should be provided in the format of a csv file for each class which will need data. The name of the file
 will identify the class, the first field the element of the class and subsequent columns the data.
 
 The loading process will be achieved by loading the csv from pandas, running a groupby on the first column and then
  iterating over the groupby object

