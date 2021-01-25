# Distretto diretto e catena di distretti

I seggi possono essere assegnati in diverse modalità, tuttavia queste modalità possono essere 
categorizzate in base alla provenienza dell'informazione utilizzata dal livello che decide chi sarà 
eletto

Per esempio il sistema elettorale più semplice, il maggioritario puro, sfrutta per l'assegnazione 
del singolo seggio che ogni distretto elettorale decide solo informazioni sul numero di voti 
all'interno del distretto stesso.

Ovviamente l'assegnazione di un singolo seggio non è un requisito per appartenere a questa categoria 
che chiameremo ad elezione diretta, per esempio i sistemi quale STV, ma anche solo un proporzionale 
senza circoscrizioni elettorali con liste a livello nazionale sono sistemi ad elezione diretta

Un esempio di elezione a cascata (tramite electoral lanes nel codice) può essere quello del 
rosatellum, nel quale i seggi sono sì assegnati dai collegi plurinominali ma in maniera tale da 
garantire la proporzionalità a livello nazionale

## Elezione diretta
Le uniche informazioni di cui necessitiamo per poter definire questo tipo di processo sono:

+ Il numero di seggi (che può essere fissato o variabile alla definizione, ma non variabile post 
votazione)
+ Il totale dei voti espressi al suo interno
+ Un algoritmo di decision

Per come è strutturato il framework il totale dei voti espressi sarà rappresentato da un dataframe 
pandas che dovrà presentare 

# Elezione e proposta

Un sistema elettorale può tollerare la presenza di un singolo individuo quale candidato per più 
seggi, tuttavia ogni individuo può essere eletto in un solo seggio.

Per evitare conflitti quando un distretto giunge ad una decisione su chi verrà eletto dovrà stilare 
una lista di candidati in ordine di "eliggibilità", il distretto proporrà ai primi n candidati il
seggio e allegherà un riferimento a questa lista (che si comporta come un iteratore)

# Candidati, partiti e coalizioni

A livello politico (contrapposto al livello geografico dei vari distretti) ci sono tre entità

+ Candidati, singoli individui che ricevono e accettano proposte dei seggi in cui sono candidati
+ Partiti, organizzazioni cui i singoli candidati appartengono, generalmente quanti più voti il 
partito ottiene tanto maggiore è la probabilità che avrà uno dei suoi candidati di essere eletto
+ Coalizioni, sono alleanze tra partiti diversi che possono essere costituite per motivi diversi, 
due esempi sono:
	+ Per superare una soglia di sbarramento
	+ Per raggruppare voti ed evitare che vengano sprecati

È importante notare che l'unico essenziale (da un punto di vista concettuale) è il candidato, partiti
e coalizioni altro non sono che intermediari tra i voti e i candidati

Cosa ci serve sapere di un candidato? Dobbiamo sapere se è presente in un distretto, se è già stato
eletto e deve poter ricevere e accettare/inoltrare una proposta

Ipotizziamo le seguenti funzioni:

+ Candidato.inDistrict :: District -> Boolean
+ Candidato.propose :: District -> Boolean
+ Candidato.elect :: () -> District + Side effect

Al livello superiore abbiamo i partiti, questi non possono assumere seggi direttamente ma ricevono un
certo numero di seggi che verranno assegnati ai loro candidati

Per ogni
