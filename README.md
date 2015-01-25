#Evaluation
##Time Measurements
The time measurements were taken by running the scripts on a desktop computer having the following characteristics:
* CPU: AMD Phenom II X4 965
* RAM: 12GB DDR3
* OS: Ubuntu Linux 14.04, kernel version: 3.13.0-44-generic

##Querying the RDF-type Summary Graph
The execution of a query against an RDF-type summary graph consists of three steps:

1. identification of the given typed nodes,
1. calculation of the shortest path between these nodes and
1. conversion of the path to the corresponding SPARQL 1.0 query.

The example query presented in the evaluation section of the paper is this:

    PREFIX dbonto: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT * WHERE {
    ?a a dbonto:MusicalWork.
    ?a ((!a)*/dbp:stylisticOrigins)|(dbp:stylisticOrigins/(!a)*) ?b.
    ?b a dbonto:MusicGenre
    }

In the following paragraphs we give a more thorough analysis of the steps involved in the execution of this query to the RDF-type summary graphs.

###Node Identification
The identification step involves retrieving a list of (possibly composite) nodes that contain the given RDF-type and selecting one from this list. Since there is no semantic difference among the nodes in the list, we can select anyone. However, we have to make sure this node exists in every RDF-type summary graph under consideration.

The example SPARQL 1.1 query presented in the evaluation section of the paper contains two RDF types, one in the triple pattern preceding the Property Path (eg. <http://dbpedia.org/ontology/MusicalWork>) and one in the final triple pattern (eg. <http://dbpedia.org/ontology/MusicGenre>). During the identification step, we choose the following common nodes of the RDF-type summary graphs respectively:

* 'http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work'
* 'http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing'

Both of the nodes are composite nodes. The '^' character is used as an RDF type delimiter inside composite nodes. The first node corresponds to <http://dbpedia.org/ontology/MusicalWork>, since it contains the same IRI. The second node corresponds to <http://dbpedia.org/ontology/MusicGenre> for the same reason. Prior to selecting these nodes we made sure they exist in every RDF-type summary graph under consideration.

##Shortest Path Calculation
After the identification step, a restricted shortest path algorithm is used in order to find the shortest path between the two nodes. The restriction imposed on the algorithm is that either the first or the last edge of a candidate shortest path must be the same as the property contained in the Property Path of the example SPARQL query (eg. <http://dbpedia.org/property/stylisticOrigins>). The algorithm is based on Dijkstra's shortest path algorithm which has a worst case complexity of O(V^2), where V is the number of nodes in the graph.

##Path to SPARQL 1.0 Conversion
In the following subsections we present the calculated shortest path and the generated SPARQL code after querying the RDF-type summary of every dataset.

###RDF-Type Summary Graph of the 1% Dataset
The shortest path found by the algorithm is:

    ['http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work',('http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work','http://dbpedia.org/ontology/genre','http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/class/yago/FusionMusicGenres^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/PopMusicGenres'),'http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/class/yago/FusionMusicGenres^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/PopMusicGenres',('http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/class/yago/FusionMusicGenres^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/PopMusicGenres','http://dbpedia.org/property/otherTopics','http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing',('http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/property/stylisticOrigins','http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing']

The path is converted to this SPARQL 1.0 code:

    SELECT DISTINCT * WHERE {
    ?_4 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_4 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_4 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Album> .
    ?_1 a <http://dbpedia.org/ontology/MusicalWork> .
    ?_1 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Work> .
    ?_3 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_3 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_3 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_2 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_2 a <http://dbpedia.org/class/yago/FusionMusicGenres> .
    ?_2 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/class/yago/PopMusicGenres> .
    ?_3 <http://dbpedia.org/property/stylisticOrigins> ?_4 .
    ?_1 <http://dbpedia.org/ontology/genre> ?_2 .
    ?_2 <http://dbpedia.org/property/otherTopics> ?_3 .
    }

### RDF-Type Summary Graph of the 10% Dataset
The shortest path found by the algorithm is:

    ['http://dbpedia.org/ontology/Album\nhttp://dbpedia.org/ontology/MusicalWork\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Work',('http://dbpedia.org/ontology/Album\nhttp://dbpedia.org/ontology/MusicalWork\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Work','http://dbpedia.org/ontology/artist','http://dbpedia.org/class/yago/JapaneseIndieRockGroups\nhttp://dbpedia.org/ontology/Band\nhttp://dbpedia.org/ontology/Organisation\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/JapaneseRockMusicGroups'),'http://dbpedia.org/class/yago/JapaneseIndieRockGroups\nhttp://dbpedia.org/ontology/Band\nhttp://dbpedia.org/ontology/Organisation\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/JapaneseRockMusicGroups',('http://dbpedia.org/class/yago/JapaneseIndieRockGroups\nhttp://dbpedia.org/ontology/Band\nhttp://dbpedia.org/ontology/Organisation\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/JapaneseRockMusicGroups','http://dbpedia.org/ontology/genre','http://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing',('http://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/ontology/stylisticOrigin','http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/HardcorePunkGenres'),'http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/HardcorePunkGenres',('http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/HardcorePunkGenres','http://dbpedia.org/property/stylisticOrigins','http://dbpedia.org/class/yago/PunkGenres\nhttp://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/class/yago/PunkGenres\nhttp://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing']

The path is converted to this SPARQL 1.0 code:

    SELECT DISTINCT * WHERE {
    ?_5 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_5 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_5 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_4 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_4 a <http://dbpedia.org/class/yago/FusionMusicGenres> .
    ?_4 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_4 a <http://dbpedia.org/class/yago/HardcorePunkGenres> .
    ?_1 a <http://dbpedia.org/ontology/Album> .
    ?_1 a <http://dbpedia.org/ontology/MusicalWork> .
    ?_1 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Work> .
    ?_3 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_3 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/class/yago/JapaneseIndieRockGroups> .
    ?_2 a <http://dbpedia.org/ontology/Band> .
    ?_2 a <http://dbpedia.org/ontology/Organisation> .
    ?_2 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/class/yago/JapaneseRockMusicGroups> .
    ?_3 <http://dbpedia.org/ontology/stylisticOrigin> ?_4 .
    ?_4 <http://dbpedia.org/property/stylisticOrigins> ?_5 .
    ?_1 <http://dbpedia.org/ontology/artist> ?_2 .
    ?_2 <http://dbpedia.org/ontology/genre> ?_3 .
    }

###RDF-Type Summary Graph of the 50% Dataset
The shortest path found by the algorithm is:

    ['http://dbpedia.org/ontology/Album\nhttp://dbpedia.org/ontology/MusicalWork\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Work',('http://dbpedia.org/ontology/Album\nhttp://dbpedia.org/ontology/MusicalWork\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Work','http://dbpedia.org/property/artist','http://dbpedia.org/ontology/Band\nhttp://dbpedia.org/class/yago/MusicalGroupsEstablishedIn2002\nhttp://dbpedia.org/class/yago/2000sMusicGroups\nhttp://dbpedia.org/ontology/Organisation\nhttp://dbpedia.org/class/yago/BostonMusicalGroups\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/AmericanPunkRockGroups'),'http://dbpedia.org/ontology/Band\nhttp://dbpedia.org/class/yago/MusicalGroupsEstablishedIn2002\nhttp://dbpedia.org/class/yago/2000sMusicGroups\nhttp://dbpedia.org/ontology/Organisation\nhttp://dbpedia.org/class/yago/BostonMusicalGroups\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/AmericanPunkRockGroups',('http://dbpedia.org/ontology/Band\nhttp://dbpedia.org/class/yago/MusicalGroupsEstablishedIn2002\nhttp://dbpedia.org/class/yago/2000sMusicGroups\nhttp://dbpedia.org/ontology/Organisation\nhttp://dbpedia.org/class/yago/BostonMusicalGroups\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/class/yago/AmericanPunkRockGroups','http://dbpedia.org/property/origin','http://dbpedia.org/ontology/PopulatedPlace\nhttp://dbpedia.org/class/yago/Country108544813\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Place\nhttp://dbpedia.org/class/yago/StatesOfTheUnitedStates\nhttp://dbpedia.org/ontology/AdministrativeRegion'),'http://dbpedia.org/ontology/PopulatedPlace\nhttp://dbpedia.org/class/yago/Country108544813\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Place\nhttp://dbpedia.org/class/yago/StatesOfTheUnitedStates\nhttp://dbpedia.org/ontology/AdministrativeRegion',('http://dbpedia.org/ontology/PopulatedPlace\nhttp://dbpedia.org/class/yago/Country108544813\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Place\nhttp://dbpedia.org/class/yago/StatesOfTheUnitedStates\nhttp://dbpedia.org/ontology/AdministrativeRegion','http://dbpedia.org/property/flower','http://dbpedia.org/ontology/Plant\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Eukaryote\nhttp://dbpedia.org/ontology/Species'),'http://dbpedia.org/ontology/Plant\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Eukaryote\nhttp://dbpedia.org/ontology/Species',('http://dbpedia.org/ontology/Plant\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/Eukaryote\nhttp://dbpedia.org/ontology/Species','http://dbpedia.org/ontology/binomialAuthority','http://dbpedia.org/ontology/Person\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/MusicalArtist\nhttp://dbpedia.org/ontology/Artist'),'http://dbpedia.org/ontology/Person\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/MusicalArtist\nhttp://dbpedia.org/ontology/Artist',('http://dbpedia.org/ontology/Person\nhttp://www.w3.org/2002/07/owl#Thing\nhttp://dbpedia.org/ontology/MusicalArtist\nhttp://dbpedia.org/ontology/Artist','http://dbpedia.org/property/genre','http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/MetalSubgenres\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/MetalSubgenres\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing',('http://dbpedia.org/ontology/MusicGenre\nhttp://dbpedia.org/class/yago/MetalSubgenres\nhttp://dbpedia.org/class/yago/FusionMusicGenres\nhttp://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/property/stylisticOrigins','http://dbpedia.org/class/yago/PunkGenres\nhttp://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/class/yago/PunkGenres\nhttp://dbpedia.org/ontology/MusicGenre\nhttp://www.w3.org/2002/07/owl#Thing']

The path is converted to this SPARQL 1.0 code:

    SELECT DISTINCT * WHERE {
    ?_5 a <http://dbpedia.org/ontology/Person> .
    ?_5 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_5 a <http://dbpedia.org/ontology/MusicalArtist> .
    ?_5 a <http://dbpedia.org/ontology/Artist> .
    ?_4 a <http://dbpedia.org/ontology/Plant> .
    ?_4 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_4 a <http://dbpedia.org/ontology/Eukaryote> .
    ?_4 a <http://dbpedia.org/ontology/Species> .
    ?_7 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_7 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_7 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_6 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_6 a <http://dbpedia.org/class/yago/MetalSubgenres> .
    ?_6 a <http://dbpedia.org/class/yago/FusionMusicGenres> .
    ?_6 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Album> .
    ?_1 a <http://dbpedia.org/ontology/MusicalWork> .
    ?_1 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Work> .
    ?_3 a <http://dbpedia.org/ontology/PopulatedPlace> .
    ?_3 a <http://dbpedia.org/class/yago/Country108544813> .
    ?_3 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_3 a <http://dbpedia.org/ontology/Place> .
    ?_3 a <http://dbpedia.org/class/yago/StatesOfTheUnitedStates> .
    ?_3 a <http://dbpedia.org/ontology/AdministrativeRegion> .
    ?_2 a <http://dbpedia.org/ontology/Band> .
    ?_2 a <http://dbpedia.org/class/yago/MusicalGroupsEstablishedIn2002> .
    ?_2 a <http://dbpedia.org/class/yago/2000sMusicGroups> .
    ?_2 a <http://dbpedia.org/ontology/Organisation> .
    ?_2 a <http://dbpedia.org/class/yago/BostonMusicalGroups> .
    ?_2 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/class/yago/AmericanPunkRockGroups> .
    ?_1 <http://dbpedia.org/property/artist> ?_2 .
    ?_3 <http://dbpedia.org/property/flower> ?_4 .
    ?_6 <http://dbpedia.org/property/stylisticOrigins> ?_7 .
    ?_2 <http://dbpedia.org/property/origin> ?_3 .
    ?_4 <http://dbpedia.org/ontology/binomialAuthority> ?_5 .
    ?_5 <http://dbpedia.org/property/genre> ?_6 .
    }

###RDF-Type Summary Graph of the 100% Dataset
The shortest path found by the algorithm is:

    ['http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work',('http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work','http://dbpedia.org/property/artist','http://dbpedia.org/class/yago/MurderedHipHopMusicians^http://dbpedia.org/class/yago/SouthernHipHopMusicians^http://dbpedia.org/class/yago/MurderedEntertainers^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/Rapper110507482^http://dbpedia.org/class/yago/MusiciansOfNewOrleans^http://dbpedia.org/ontology/Artist^http://dbpedia.org/class/yago/Artist109812338^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Person^http://dbpedia.org/class/yago/SouthernRappers^http://dbpedia.org/class/yago/AmericanMurderVictims^http://dbpedia.org/class/yago/AfricanAmericanRappers'),'http://dbpedia.org/class/yago/MurderedHipHopMusicians^http://dbpedia.org/class/yago/SouthernHipHopMusicians^http://dbpedia.org/class/yago/MurderedEntertainers^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/Rapper110507482^http://dbpedia.org/class/yago/MusiciansOfNewOrleans^http://dbpedia.org/ontology/Artist^http://dbpedia.org/class/yago/Artist109812338^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Person^http://dbpedia.org/class/yago/SouthernRappers^http://dbpedia.org/class/yago/AmericanMurderVictims^http://dbpedia.org/class/yago/AfricanAmericanRappers',('http://dbpedia.org/class/yago/MurderedHipHopMusicians^http://dbpedia.org/class/yago/SouthernHipHopMusicians^http://dbpedia.org/class/yago/MurderedEntertainers^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/class/yago/Rapper110507482^http://dbpedia.org/class/yago/MusiciansOfNewOrleans^http://dbpedia.org/ontology/Artist^http://dbpedia.org/class/yago/Artist109812338^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Person^http://dbpedia.org/class/yago/SouthernRappers^http://dbpedia.org/class/yago/AmericanMurderVictims^http://dbpedia.org/class/yago/AfricanAmericanRappers','http://dbpedia.org/property/associatedActs','http://dbpedia.org/ontology/Person^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Artist'),'http://dbpedia.org/ontology/Person^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Artist',('http://dbpedia.org/ontology/Person^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/MusicalArtist^http://dbpedia.org/ontology/Artist','http://dbpedia.org/property/genre','http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/MusicGenres^http://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/MusicGenres^http://www.w3.org/2002/07/owl#Thing',('http://dbpedia.org/ontology/MusicGenre^http://dbpedia.org/class/yago/MusicGenres^http://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/property/stylisticOrigins','http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing'),'http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing']

The path is converted to this SPARQL 1.0 code:

    SELECT DISTINCT * WHERE {
    ?_5 a <http://dbpedia.org/class/yago/PunkGenres> .
    ?_5 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_5 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_4 a <http://dbpedia.org/ontology/MusicGenre> .
    ?_4 a <http://dbpedia.org/class/yago/MusicGenres> .
    ?_4 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Album> .
    ?_1 a <http://dbpedia.org/ontology/MusicalWork> .
    ?_1 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_1 a <http://dbpedia.org/ontology/Work> .
    ?_3 a <http://dbpedia.org/ontology/Person> .
    ?_3 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_3 a <http://dbpedia.org/ontology/MusicalArtist> .
    ?_3 a <http://dbpedia.org/ontology/Artist> .
    ?_2 a <http://dbpedia.org/class/yago/MurderedHipHopMusicians> .
    ?_2 a <http://dbpedia.org/class/yago/SouthernHipHopMusicians> .
    ?_2 a <http://dbpedia.org/class/yago/AmericanMurderVictims> .
    ?_2 a <http://dbpedia.org/class/yago/MurderedEntertainers> .
    ?_2 a <http://dbpedia.org/class/yago/Rapper110507482> .
    ?_2 a <http://dbpedia.org/class/yago/MusiciansOfNewOrleans> .
    ?_2 a <http://dbpedia.org/ontology/Artist> .
    ?_2 a <http://www.w3.org/2002/07/owl#Thing> .
    ?_2 a <http://dbpedia.org/ontology/MusicalArtist> .
    ?_2 a <http://dbpedia.org/ontology/Person> .
    ?_2 a <http://dbpedia.org/class/yago/SouthernRappers> .
    ?_2 a <http://dbpedia.org/class/yago/Artist109812338> .
    ?_2 a <http://dbpedia.org/class/yago/AfricanAmericanRappers> .
    ?_3 <http://dbpedia.org/property/genre> ?_4 .
    ?_4 <http://dbpedia.org/property/stylisticOrigins> ?_5 .
    ?_1 <http://dbpedia.org/property/artist> ?_2 .
    ?_2 <http://dbpedia.org/property/associatedActs> ?_3 .
    }

##Query Execution Time Decrease
Here we give an explanation of the query execution time decrease at the final point in the plot. The time measurement depends mainly on the running time of the shortest-path algorithm. Since the 50% dataset contains less triples than the 100% dataset, the corresponding RDF-type summary graphs may contain different shortest paths between the same endpoints. This means that the algorithm would have to examine more nodes (in the RDF-type summary graph of the 50% dataset) in order to find the shortest path. As a result, the query execution time could be greater in the 50% dataset than in the 100% dataset. Therefore, the execution time of the navigational query is independant of the RDF graph size. Instead, it depends on the size of the RDF-type summary which, in turn, is proportional to the number of predicates it contains.

If there is no path between the endpoints, the Dijkstra algorithm is expected to take more time to finish due to visiting a greater number of nodes.

#Repository Contents
In this repository you can find links to the DBPEDIA datasets that were used for the evaluation of the paper.
##Dataset links
The datasets used for the evaluation can be downloaded from the links below:
* The 100% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_100.nt.bz2
* The 50% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_50.nt.bz2
* The 10% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_10.nt.bz2

The 1% DBPEDIA dataset can be created from the 10% dataset by keeping the first 1537384 triples. This is done by executing this command:

    head -1537384 benchmark_10.nt > benchmark_1.nt

##Automated evaluation script
We have prepared a script that takes as input the 4 DBPEDIA datasets (namely benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt) and creates all RDF-type summary graphs, executes the example query against the graphs, measures execution time and creates the scalability plot. The script can be found at [automated_evaluation.py](https://github.com/SWRG/ESWC2015-paper-evaluation/blob/master/automated_evaluation.py).
Before executing the script make sure networkx and gnuplot are installed in the system. To install these packages on an Ubuntu 14.04 platform, just give the following command:

    sudo apt-get install gnuplot, python-networkx

The dataset files benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt must be in the same directory. The automated evaluation script is executed with the command:

    python automated_evaluation.py DATASET_DIR

where DATASET_DIR is the directory that contains the datasets. The script stores the RDF-type summary graphs in the same directory. In addition, it creates a directory named 'evaluationdata' where it stores the scalability plot along with the corresponding data.

The most time consuming step of the evaluation is the RDF-type summary creation. In our setup, the creation time of each dataset was:

1. for the 1% dataset: 4min
1. for the 10% dataset: 17min
1. for the 50% dataset: 90min
1. for the 100% dataset: 210min