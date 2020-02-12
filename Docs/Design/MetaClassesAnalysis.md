# Objective

Determining which metaclasses are actually needed and which are superfluous, this will be done by
analysing the various classes

# Rosatellum

+ Uninominale: eleggi
+ Plurinominale: eleggi, proponi
+ Regione
+ Circoscrizione: proponi, correggi
+ Sezione
+ Coalizione
+ Partito
+ Candidato


# Metaclasses

## Geoent

A geoent represents a geographical subdivision of the electoral process, in its most basic form it
should just allow to tell whether someone is elected in it.

A geoent must, by default, be able to tell who has been elected in it or in its subdivisions. This
is handled by the hub mostly but the class itself must have a function to call

Provided functionalities:

+ `electedIn`


## Polent

A polent represents a political part of the process, it represents a certain layer of abstraction 
over candidates/representatives, candidates themselves, parties and coalitions are all polents
