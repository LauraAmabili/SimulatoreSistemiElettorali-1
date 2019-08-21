# Overview

The simulation works in different phases:
1. Loading classes and packages.  
The program needs to load and name all the different Metaclasses and functions which will be used in the execution
 phase, metaclasses are loaded in the Metaclasses package and functions and classes in the Commons package
2. Loading the configuration files.  
There are different configuration files for each simulation to be run. In the loading order they are:
    1. Class configuration: This file will make use of the metaclasses system and others to define the behaviour of
     classes involved in the simulation.
    2. Instance configuration, this will create the various class instances and fill them appropriately, except for
     the data source classes, for instance in this phase the Plurinominale class instances will be created by specifying
      the seats it has to distribute as well as the uninominal districts under it. Similarly parties will be told to
       which coalition they belong and candidates their parties and districts.  
       Because these configurations are heterogeneous in nature this will be provided by multiple files which will be
        concatenated. T
    3. Polling data, this is the data that will fill the data sources, I decided
3. Determine Lane ordering
4. Execute each lane iteratively

