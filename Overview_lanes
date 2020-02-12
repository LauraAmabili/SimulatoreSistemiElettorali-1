exec lane ->
	1. Raccogli proposte
	2. Determina ideale
	3. Correggi
	4. Ripeti as needed

exec lane head:
	1. Raccogli
	2. Ideale
	3. Correggi
	4. Ripeti
	5. Inoltra a sottolivelli

exec lane node
	1. Raccogli
	2. Deriva ideale da sopra
	3. Correggi
	4. Ripeti
	5. Inoltra

exec lane tail
	1. Ricevi distribuzione
	2. Registra information
	3. Return

exec lane only:
	1. Determina ideale
	2. Registra information
	3. Return

Information model:

Informazione generale:
Dict[
	PolEnt_nome,
	Dict[
		str: object
		]
	]

Quando exec lane viene chiamata viene chiamata con una lista di "informazioni generali"

Nella fase di raccolta e ideale possono avvenire due cose:
1. Si genera nuova informazione ideale
2. Si genera informazion valida solo in subsection specifiche

Informazione specifica:
Dict[
	Geo_ent_nome,
	Informazione generale
	]

Propose restituisce quindi:
1. Distribuzione
2. Informazione generale
3. Informazioni specifiche

Quando ci sono più operazioni sostituisco la distribuzione ma concateno le informazioni

-------------

Le operazioni in comune tra tutti sono:

+ ciclo ideale-collect-correct
	Facendo sempre riferimento alla distribuzione precedente
+ 



---------

Call order

lane_exec(lane, *info, distribution)
	Chiama:
		- propose, senza cambiamenti
		- correct, fornendo una distribuzione ideale e un dizionario di distribuzioni

	Se c'è un constraint devo poter dire che deve fare una proposta in base alle liste
	Un constraint sulle proposte può essere di due tipi 

correct(ideal, actual, info_specific, *info_general)
	Restituisce:
		- distribution
		- info_specific_updated
		- info_general

propose(


---------

Le distribuzioni devono rimanere in formato dataframe

La distribuzione è sempre un dataframe con due colonne:
	+ Una colonna che indica cosa sta venendo eletto, una colonna di stringhe
	+ Una colonna di interi chiamata Seats

Le informazioni come sopra

Tutte le stringhe, sia informazioni che colonne eletti sono PolEnts

--------

Operazioni:

Prima di effettuare un'operazione ho:

+ Distribuzione
+ Lista di informazioni

# Distribuzione:

### None
Quando sono in lane head devo per forza ricavarla

### Ideale:
Dict[str, int], questo è quello che si ha prima di tutte le operazioni prima di correggere le 
distribuzioni raccolte

### Composta:

Dict[str, Dict[str, int]], questo è quello che si ottiene quando si corregge una distribuzione
ideale

# Informazioni:

Le informazioni sono:

+ generate da propose
+ passate ai livelli inferiori
+ modificate da correct
+ passate a correct

Propose le 





## Comuni
Una lista di dizionari che arriva da sopra, più l'indice è basso più è recente è l'informazione,
ogni indice è un livello



## Specifiche
Le informazioni in posizione 0 sono le informazioni 

--------------

Esempio di info in rosatellum

Nazione:

+ ideale:
	+ crea Nazione
+ collect:
	+ raccogli RestoCoalCircoscrizione
	+ raccogli RestoCoalCircoscrizioneUsato
+ correggi:
	+ modifica RestoCoalCircoscrizioneUsato
+ collect (2):
	+ raccogli RestoListaCircoscrizione
	+ raccogli RestoListaCircoscrizioneUsato
+ correggi:
	+ modifica RestoListaCircoscrizioneUsato


Circorscizione:

+ ideale:
+ collect:
	+ raccogli RestoListaPlurinominale 
	+ raccogli RestoListaPlurinominaleUsato
+ correggi:
	+ modifica RestoListaPlurinominaleUsato


