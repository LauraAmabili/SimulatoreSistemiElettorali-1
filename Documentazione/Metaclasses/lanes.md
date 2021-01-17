# Obiettivo Lane
La metaclasse Lanes.py è la parte centrale del sistema di distribuzione dei seggi.

Essa infatti consente di avere delle suddivisione tra i seggi totale, in cui ciascuna di queste divisioni posso utilizzare una diversa meccanica di assegnazione dei propri seggi.

Consente inoltre la creazioni di una gerarchia di livelli geografici, i quali possono prendere informazioni da eventuli livelli superiori, elaborarli e distribuire informazioni elaborate ai livelli inferiori.
Il fondo di questa gerarchia è l'assegnazioni dei seggi all'entità politica di livello più basso, quindi Candidati, Partiti o Coalizioni.

======

## Funzionalità Lane
Le lanes sono gli esecutore del sistema elettorale, questo significa che ogni lane presente inizia chiamando una funzione sulla lane head.
Il risultato di questa funzione è salvato nell'Hub e si itera su questo dato fino all'ottenimento del risultato finale.

Le lanes devono assegnare un certo numero di seggi, questo valore può essere deciso dai file di configurazione o può essere assegnato a run-time dai livelli superiori.

======

## Struttura Lanes
Consentendo di rappresentare una gerarchia di livelli geografici, a loro volta le Lanes sono strutturare in modo gerarchico :
    - Lane Head
    - Lane Node
    - Lane Tail


### Lane Head
La Lane Head è il più alto livello, è inoltre il primo che viene chiamato una volta eseguito il programma.

Questa Lane offre una funzione per la creazione della prima proposta di distribuzione dei seggi, la quale verrà poi mandata ai livelli inferiori.
Oltre alla creazione della proposta, può anche applicare correzioni e modifiche alle distribuzioni dei livelli inferiori.

### Lane Node
Questa Lane ha le stesse funzionalità della Lane Head, la sua funzione per la proposta della distribuzione è possibile chiamarla dai livelli superiori.

### Lane Tail
La Lain Tail è, invece, il più basso livello gerarchico, questo significa che non dovrà inoltrare la sua proposta di distribuzione a dei livelli inferiori, piuttosto dovrà eleggere i Candidati/Partiti/Coalizioni usando le informazioni ricevute.

### Lane Unica
Questa Lane si isola dalla gerarchia perchè non inoltra o riceve informazioni da altri livelli.
Infatti essa usa direttamente le informazioni per generare una distribuzione e assegnare i seggi.

Può essere vista come una Lane Head e una Lane Tail convergenti in un unico nodo.

======

# Schema Lanes
La metaclasse Lanes.py mette a disposizione due funzioni:
    - *exec_lane* : la quale da inizio all'esecuzione della lane
    - *propose* : la quale usando le informazioni passategli genera e restituisce una proposta di distribuzione

## Exec lane

**Introduzione al sistema di lanes**: la lane è l'unita organizzativa che
all'interno di una simulazione assegna ad un certo numero di candidati dei
seggi. Le lane sono eseguite sequenzialmente e si dividono in due tipi:
1. Multi step, queste lane rappresentano leggi elettorali nelle quali chi
viene eletto in una data circoscrizione dipende non solo dai risultati della
circoscrizione ma anche da informazioni esterne al distretto specifico. 
Per esempio la maggior parte delle leggi elettorali proporzionali assegna
i seggi ai partiti in base alla proporzione di voto nazionale, tuttavia
i candidati vengono eletti nei singoli distretti, in base ai risultati locali
2. Single step, queste lane rappresentano leggi nelle quali la distribuzione
di seggi è influenzata solo dalla distribuzione locale dei voti, l'esempio 
naturale è quello dei sistemi maggioritari, tuttavia questa classificazione si
applica anche a sistemi proporzionali dove la lista elettorale di ogni partito
sia unica e nazionale

Nel caso di Lane Head o Lane Unica, questa funzione viene chiamata dall'Hub; per Lane Node e Lane Tail la funzione sarà invece invocata dalla Lane di livello superiore.

*Input per lane_exec* :
    - Nome della Lane
    - Informazioni : questo parametro comprende più dizionari, il primo contiene informazioni specifiche del distretto che esegue la funzione ed è quindi modificabile, mentre gli altri contengono informazioni condivise ed è quindi meglio evitare la modifica di quest'ultime
    - Distribuzione : un Pandas dataframe con contenente la distribuzione di seggi dei livelli superiori. Questo dataframe conterrà le informazioni delle entità politiche e dei seggi assegnati

*Valore Ritornato da lane_exec* :
Viene restituita una lista di tuple contenenti :
    - electoral_district : l'istanza del distretto che ha effettuato l'elezione
    - lane_name : il nome della lane
    - elector : il nome dell'istanza eletta
    - seats : il numero di seggi assegnati

## Lane propose

MODIFICARE
**Funzione ad alto livello**:  
Similmente a totals queste funzioni vengono differenziate dal primo parametro 
posizionale  fornito alla chiamata

Propose viene chiamata con i seguenti parametri:
+ nome della funzione che intendo chiamare
+ *info: lista di informazioni dalla più recente alla più vecchia
+ distribution, keyword argument che indica la distribuzione già definita
+ constraint, kwarg, indica la distribuzione da rispettare (per esempio la 
distribuzione di seggi ad una lista deve rispettare la distribuzione tra
coalizioni)

i valori restituiti sono:
+ una distribuzione (dataframe con due colonne, la prima contente nomi di 
PolEnt, la seconda numeri convertibili a interi)
+ Un dizionario contenente informazioni
FINE MODIFICARE

=====

# Configurazione Lanes

## Keyword nei File .yaml
lane

## Schema nei File .yaml
La struttura della Lane viene espressa usando un dizionario dove le chiavi sono il nome della lane e i valori sono dizionari contenenti le specifiche della lane

*Contenuti dei Dizionari delle Specifiche* :

    - node_type : può assumere un valore tra
        - only : per definire una Lane Unica, non accetta parametri oltre il nome
        - head : per definire una Lane Head, ovvero la punta della gerarchia; non accetta parametri a parte il nome
        - node : per definire una Lane Node, ovvero un punto intermedio di una gerarchia
        - tail : per definire una Lane Node, ovvero il fondo della gerarchia
    
    - info_name : il nome del nodo, quando un nodo genererà informazioni allora aggiunge un'associazione chiave/valore tipo : "info_name = self.name"

    - distribution : (solo per Lane Only) il nome della propose da invocare e a cui fornire le informazioni per la generazione della distribuzione

    - order_number : (solo per Lane Only e Head) indica la priortà con cui eseguire le Lane, più basso il numero più alta la priorità

    - first_input : (solo per Lane Head) il nome della propose da invocare e a cui fornire le informazioni per la generazione della distribuzione da passare alle Lane inferiori

    - sub_level : (solo per Lane Head e Lane Node) il nome del nodo al livello inferiore a cui dovranno essere pasate le informazionoi

    - operations : (solo per Lane Head e Lane Node) una lista di dizionari che descrivono le operazioni da eseguire in sequenza per l'elaborazione della distribuzione prima d'inoltrarla al livello inferiore
    
    Schema Dizionario per Operations :
        - collect_type : il nome della propose da chiamare nei livelli inferiori
        - ideal_distribution : può essere
            - '$', per riferirsi all'ultima distribuzione valida
            - una stringa, per chiamare propose e usare la distribuzione ottenuta
            - un dizionario contenente la chiave "source" e la definizione di una funzione che prende in input il riferimento al distretto corrente e restituisce un dataframe distribuzione
        - corrector : il nome di una funzione definita in Commons (commons.nome_funzione) che riceve in input:
            - il distretto corrente
            - la distribuzione ideale
            - un dizionario contenente le distribuzioni raccolte dai livelli inferiori
            - un dizionario contenente le informazioni raccolte dai livelli inferiori
            - una lista di informazioni, il primo elemento riguarda esclusivamente il distretto corrente
 
        e restituisce:
            - un dizionario di distribuzioni da inoltrare ai livelli inferiori
            - un dizionario di informazioni da inoltrare ai livelli inferiori
            - informazioni comuni a tutti i livelli inferiori
        - collect_constraint, può essere:
            - None per non porre limitazioni alla distribuzione generata dai livelli inferiori
        - '$' per inoltrare la distribuzione corrente
        - stringa, per inoltrare il risultato di una propose del distretto corrente
        - forward_distribution, se True allora questa operazione modifica solo le informazioni e non la distribuzione

=====

# Configurazione Lane Propose

## Keyword nei File .yaml
lanes_propose

## Schema nei File .yaml
La struttura della Lane Propose viene espressa usando un dizionario dove le chiavi sono il nome della lanes_propose e i valori sono dizionari contenenti le specifiche della lanes_propose

*Contenuti dei Dizionari delle Specifiche* :

    - source : contiene una funzione (definita tramite source) che viene chiamata per fornire il punto di partenza all'estrazione di informazioni e della distribuzione. Questa funzione può essere definita in qualunque modo ma deve:
        1. Accettare i parametri a kw: information, constraint, distribution
        2. Restituire un dataframe

    - distribution : definisce come ricavare una distribuzione dal dataframe che source restituisce. Può essere:
        - una lista di due stringhe, entrambe colonne del dataframe. In questo caso la prima rappresenta la PolEnt che riceverà i seggi e la seconda i seggi assegnati
        - un dizionario

        Schema del dizionario di `distribution`:
            - key : la colonna cui associare i seggi
            - selector : viene riconosciuto da `parse_row_selector_take` o `parse_row_selector_value`
            - seats: può essere
                - un intero, in tal caso tutti i candidati validi riceveranno lo stesso numero di seggi
                - stringa, ogni candidato riceverà il numero di seggi associato alla colonna

    - info_key (opzionale): se vuoto la chiave delle info è la stessa della chiave della distribuzione, altrimenti indica la PolEnt cui associare le informazioni

    - info: una lista di stringhe rappresentanti le colonne del dataframe contenenti informazioni

Restituisce un dataframe con colonne: \[key, "Seats"\]

 




