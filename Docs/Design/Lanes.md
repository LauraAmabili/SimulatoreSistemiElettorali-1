Lanes are the system used to determine which candidates get elected according to different electoral procedures. This
 allows parallel systems (for instance assigning some seats with a proportional systems and others with a
  majoritarian with no interdependence), or parallel systems which use information from others (for instance the
   MMP system in germany uses the results of the majoritarian districts as a starting point for the proportional
    system, another example might be using majoritarian results as a criteria in the assignment of seats)

For this to work we need some further setup:
1. A record of which lanes are there, and which starting point
2. A way of accessing the results of a previously executed lane
    1. Index by both lane and distrectual division. For instance if I am looking for the uninominal results in a
     region I will query: `Hub.elected('uninominale', regione)` and explore the subdivisions (I must be careful
      regarding for instance the query `Hub.elected('uninominale', nazione)` since a simple recursion will return
       doubled results (accessing `Regione -> Uninominale` and `Circoscrizione -> Plurinominale -> Uninominale`)  
       Possible solution: The recursion will just find endpoints which are child of the given division.  
       Use try/catch to check it has the subdivision function after checking it isn't the endpoint of the lane

These requirements can be achieved by making use of the Hub structure. The hub will be created with an integrated
 lanes area. This will consist of a dictionary which will have the name of the lane as the key and will reference the
  class which is the head of the lane. Once the process reaches the bottom level this will propose the candidacy to
   every eligible candidate. After this the program will iterate over the candidates still to be elected and ask them
    to choose their seat. This will keep iterating until it reaches a fixed point (no candidate left eligible). It
     will then add the elected candidates to the record of those elected in the lane and flag them as ineligible
 
It is important that the bottom of the lane knows how to retrieve the those elected in themselves and that the lane
 knows also the type of the endpoint. This way if I want to know who has been elected in a given subdivision by a
  given process all I need is to:
  1. Find which class is the bottom for the lane
  2. Find all the subdivisions which are distinct instances of the aforementioned class
  3. Call the function on them and merge the result accordingly

To recap in the hub I will have:
+ Name of the lane
+ Starting point of the lane
+ End point of the lane
+ For each endpoint the list of associated representatives