Progetto di Ingegneria Informatica: **Simulatore di sistemi elettorali**

# Obiettivi

Questo progetto si prefigge di sviluppare un framework che faciliti il processo di modellazione 
di un sistema elettorale e la simulazione dei risultati elettorali ottenuti applicando il sistema
a dati scrutinati, siano essi dati generati manualmente o risultati di una vera elezione

Tali simulazioni potrebbero essere effettuate per valutare l'impatto di una variazione di sistema 
elettorale sulla rappresentanza politica in un territorio, tali variazioni potrebbero per esempio
essere il passaggio da una legge di natura proporzionale ad una di natura maggioritaria, ovvero
la rimozione o variazione di una soglia di sbarramento in una legge di natura proporzionale.

Alternativamente si potrebbe voler studiare, a parità di sistema elettorale, gli effetti di una
diminuzione di seggi o di una variazione dei collegi elettorali.

Infine si potrebbero voler simulare i risultati di un'elezione dato un sondaggio

Con il sistema qui sviluppato la definizione del funzionamento di un sistema elettorale è 
semplificata attraverso l'adozione di una sintassi semplificata che richiede la minor quantità di
codice possibile, rimanendo tuttavia estendibile tramite python puro dove tale flessibilità sia
necessaria

## Limitazioni e ipotesi adottate

Volendo mantenere la sintassi definita il più semplice possibile le funzionalità definite in
questo progetto sono concentrate su sistemi a singolo turno, escludendo quindi i sistemi
che prevedono ballottaggi (per esempio il modello francese) o quei sistemi a turni multipli 
virtuali quali il modello irlandese.

Tuttavia questi modelli possono essere studiati integrando con del codice python ad-hoc che simuli
il doppio turno chiamando ripetutamente questo modulo, o scrivendo manualmente delle funzioni che
simulino il processo di trasferimento delle preferenze del sistema irlandese

Infine questo sistema permette di avere due sistemi elettorali operanti in parallelo, quali il
sistema plurinominale e quello uninominale della legge Rosato o del sistema tedesco; tuttavia si
presuppone che la struttura sia omogenea, pertanto non è possibile simulare direttamente leggi 
elettorali diverse operanti su aree geografiche diverse.

Il sistema non è pertanto orientato a supportare elezioni quali le elezioni per il parlamento
europeo (avendo 27 leggi elettorali diverse) o le presidenziali americane (permette tuttavia
di simulare il processo di elezioni presidenziali nei 48 stati che assegnano i loro voti nella
medesima maniera)

# Funzionalità 

Il programma prevede 4 livelli di configurazione

1. Codice sorgente, modificando il contenuto delle cartelle src/Metaclasses e src/Commons si può 
modificare il comportamento di base del programma, tuttavia questo tipo di modifica, sebbene 
possibile è superfluo per quanto riguarda src/Metaclasses nei casi considerati e limitato a
inserire in src/Commons file contenenti funzioni cui ci si riferisce nelle configurazini di classe
2. Definizione di classi, tramite file yaml (o file python per classi più complesse).
Tramite questi file si definisce il comportamento di ogni componente, questi corrispondono alla
legge elettorale che si intende modellare
3. Definizione di istanze, tramite file yaml. Questi file definiscono con che parametri creare le
istanze delle classi definite al punto precedente e corrispondono (nel mondo reale) alla 
definizione delle circoscrizioni elettorali, del numero di seggi da distribuire e alle
dichiarazioni delle varie liste e dei candidati che parteciperanno alle elezioni
4. Definizione dei risultati delle votazioni tramite file csv, questi forniscono alle classi di
competenza il risultato delle votazioni, siano essi risultati veri o simulati

Una volta elaborate queste informazioni il programma simula il risultato delle elezioni
restituendo una lista di candidati eletti.

Questa lista conterrà per ogni candidato eletto il nome e il partito di appartenenza

## Input del programma:
+ path della configurazione, una cartella contenente le cartelle:
    + class
    + instance
    + data 

## Configurazione classi:
Nella cartella ci possono essere file del tipo:
+ Nome_classe.yaml o
+ Nome_classe.py

Considero prima tutti i file python, 

## Configurazione istanze:

## Dati elezione:



# Architettura software






















