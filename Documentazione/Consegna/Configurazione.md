# Configurazione delle Classi
Credits: Lorenzo Ruffati 

---
## Source_Parse
#### Funzionalità
Questa non è una metaclasse, non può essere inserita tra le `metaclasses` da importare all'inizio del file.
Tuttavia i file di configurazione, prima di essere usati per creare la classe, vengono analizzati da questa funzione, la quale cerca ogni la parola chiave `source` e, dove trovata, la sostituisce con una funzione chiamabile.
Tale funzione può quindi restituire un qualunque valore come specificato nella configurazione.

#### Configurazione
*Parametri :* source può avere come valore associato sia uno scalare (intero, booleano o stringa), nel qual caso la funzione restituirà tale scalare, sia un dizionario con le seguenti chiavi:
+ `type` : può essere
    + `fun` : per indicare che il risultato sarà ottenuto chiamando una funzione
    + `att` : per indicare che il risultato sarà un attributo o una variabile
    + `kwarg` : per indicare che il risultato sarà un argomento a keyword del namespace originale
+ `columns` : una lista di stringhe nella forma: `colonna( -> nuovo_nome)`, presuppone che il risultato sia un dataframe e restituisce solo la slice formata dalle colonne specificate (nell'ordine specificato) eventualmente con il nome modificato
+ `rename` : un dizionario del tipo: `colonna: nuovo_nome`, assume un risultato di tipo dataframe e rinomina le colonne usando il dizionario. In un conflitto tra rename implicito nelle columns e esplicito in rename il rename specificato in questo dizionario ha precedenza :
+ `store` : una stringa nella forma
    + `#nome` il risultato sarà salvato in `self.nome`
    + `$nome.chiave` il risultato sarà salvato nel dizionario `nome` come `chiave`
    + `nome` il risultato sarà aggiunto al namespace nella variabile `nome`
+ `options` : una lista di stringhe che modificano il comportamento
    + `NoForward`, se presente, non inoltra gli argomenti posizionali e a keyword con cui si chiama `source` alle funzioni sottostanti
    
Solo per type `fun` :
+ `name` : il nome della funzione (viene trovata facendo `eval(name, globals(), locals)`)
+ `args` : una lista di valori accettabili come configurazioni di source, passati come argomenti posizionali
+ `kwargs` : come args ma un dizionario con chiavi stringhe e passato come kwargs

---
## External

#### Funzionalità
In questa metaclasse vengono definite le variabili della classe creata, i loro valori saranno poi presi dai file d’instanziazione o da funzione specifiche.
Per ogni variabile è inoltre creato il corrispettivo metodo d'accesso.

#### Configurazione
*Parola Chiave nel File :* `external`

*Parametri :*  sono strutturati in un dizionario avente come chiavi delle stringhe che diventeranno poi i nomi delle variabili.
I valori associati alle chiavi sono dizionari aventi le seguenti chiavi :
+ `init` : opzionale, valore di default `False`
+ `default` : opzionale, compare solo dove `init` è `True` e indica il 
valore di default della variabile
+ `targets` : opzionale, il valore associato è una lista di dizionari in cui ogni dizionario genera una funzione che accede alla stessa variabile ma restituisce informazioni diverse

Le seguenti chiavi sono mutualmente esclusive con `targets`:
+ `name` : opzionale, di default il valore della chiave di primo livello, 
indica che nome dare alla funzione di accesso
+ `columns` : opzionale, indica quali colonne restituire
+ `type` : opzionale, converte il risultato, può essere:
    + `int`
    + `float`
    + il nome di una classe definita dall'utente

Le chiavi del dizionario interno a `targets` sono :
+ `name`
+ `columns`

*Risultati :* vengono generate le variabili e le funzioni con il seguente schema :
+ `give_{chiave_del_dizionario}`
+ `get_{chiave_del_dizionario_o_name_o_chiave_di_external}`
+ se `init` è `True` allora aggiunge un valore che è richiesto in fase di istanziazione, a meno che default sia presente, in tal caso inserisce il valore di default


---
## Superdivision
#### Funzionalità
Questa metaclasse definisce la relazione tra due classi geografiche specificando quali variabili della classe identificano il sottolivello, di che tipo è il sottolivello e quali funzioni esporre dal sottolivello.

Questa metaclasse definisce le relazioni tra due classi di aree geografiche e identificando il sottolivello, il tipo del sottolivello e consente inoltre di esporre delle funzioni del sottolivello in modo che possano essere chiamate anche dal livello superiore.

*Parola Chiave nel File :* `subdivisions`

*Parametri :* un dizionario le cui chiavi indicano il nome della variabile in cui salvare l'istanza del sottolivello.
Ad ogni chiave viene associato un dizionario avente la seguente configurazione :
+ `type` : il nome della classe
+ `functions` : una lista di dizionari, ogni dizionario ha :
    + `name` : il nome della funzione da esporre
    + `source` : una definizione tramite source della funzione da eseguire. Si assume che nell'esecuzione di source "self" nel namespace si riferirà ad una sottodivisione

La funzione verrà chiamata su ogni istanza del sottolivello e i risultati saranno aggregati :
+ se di tipo `int` verranno sommati
+ se di tipo `DataFrame` verranno concatenati
+ altrimenti concatenati in una lista

---
## Lanes
Si suddivide in due parti :
- lane
- lanes_propose
<br>

### Lane
#### Funzionalità
Questa parte della configurazione permette la configurazione e creazione della funzione exec_lane nella classe.
La funzione ha lo scopo di iniziare l'esecuzione della lane su cui è stata chiamata, l'inizio dell'elaborazione dei dati è reso possibile grazie alla chiamata di questa funzione tramite l'Hub.
La funzione riceve in input le seguenti informazioni:
+ `name` : nome della lane
+ `*informazioni` : una lista di dizionari
    - il primo dizionario  rappresenta le informazioni riguardanti lo specifico distretto  che sta eseguendo la funzione, è consentito modificarlo
    - i dizionari successivi sono condivisi tra i distretti e non modificabili
+ `distribution` : un dataframe contenente la distribuzione di seggi generata ai livelli superiori. La prima colonna è una colonna contiene i nomi di una PolEnt di classe Elector, la seconda colonna una lista di numeri convertibili in interi rappresentante il numero di seggi assegnati all'entità politica.

#### Configurazione

*Parola Chiave nel File :* `Lane`

*Parametri :* un dizionario dove le chiavi sono i nomi delle lane.
I valori associati alle chiavi sono dizionari aventi le seguenti chiavi :
+ `node_type` : Uno tra
    + `only` : specifica una lane single step, non ha parametri oltre il nome
    + `head` : il punto di partenza di una lane multi step
    + `node` : un generico punto intermedio di una lane multi-step
    + `tail` : il nodo finale di una lane multi-step
+ `info_name` : ogni nodo aggiunge alle informazioni generate nel nodo stesso una coppia chiave/valore del tipo `info_name = self.name`

Solo per lane `only`:
`distribution` : il nome della propose da chiamare per la generazione della distribuzione

Solo per only e `head` :
`order_number` : indica la priorità d'esecuzione della lane

Solo per `head` :
+ `first_input` : rappresenta il punto di partenza per le operazioni da effettuare

Solo per `head` e `node` :
+ `sub_level` : indica il tipo del nodo al livello inferiore
+ `operations` : una lista di dizionari che specificano delle operazioni, queste operazioni sono concatenate per trasformare una distribuzione di input in una da passare al livello inferiore e per generare informazioni aggiuntive

Definizione del dizionari di `operations` :
+ `collect_type`: Il tipo di propose da chiamare per raccogliere proposte dai livelli inferiori
+ `ideal_distribution`: può essere
    + `$` : per riferirsi all'ultima distribuzione valida
    + `nome_di_propose` : per chiamare propose e usare la distribuzione ottenuta
    + un dizionario contenente la chiave `source` e la definizione di una funzione che prende in input il riferimento al distretto corrente e restituisce un dataframe distribuzione
+ `corrector` : una funzione definita in commons che
    - riceve in input:
        + il distretto corrente
        + la distribuzione ideale
        + un dizionario contenente le distribuzioni raccolte dai livelli inferiori
        + un dizionario contenente le informazioni raccolte dai livelli inferiori
        + una lista di informazioni, il primo elemento riguarda esclusivamente il distretto corrente
 
    - restituisce:
        + un dizionario di distribuzioni da inoltrare ai livelli inferiori
        + un dizionario di informazioni da inoltrare ai livelli inferiori
        + informazioni comuni a tutti i livelli inferiori
+ `collect_constraint` : che può avere i valori :
    + `None` : per non porre limitazioni alla distribuzione generata dai livelli inferiori
    + `$` : per inoltrare la distribuzione corrente
    + `nome_di_una_propose` : per inoltrare il risultato della propose avente il nome specificato del distretto corrente
+ `forward_distribution` : se `True` allora questa operazione modifica solo le informazioni e non la distribuzione

*Risultato :* il risultato della funzione è una lista di tuple con i seguenti campi :
+ `electoral_district` : distretto che ha effettuato l'elezione
+ `lane_name` : il nome della lane
+ `elector` : colui che ha preso i seggi
+ `seats` : il numero di seggi

<br>
### Lanes_Propose
#### Funzionalità
Queste parte definisce la struttura della distribuzione di ritorno e quale funzione chiamare per generare la distribuzione.

Propose viene chiamata con i seguenti parametri:
+ nome della funzione che intendo chiamare
+ `info` : lista di informazioni dalla più recente alla più vecchia
+ `distribution` : indica la distribuzione già definita
+ `constraint` : kwarg, indica la distribuzione da rispettare (per esempio la distribuzione di seggi ad una lista deve rispettare la distribuzione tra coalizioni)

#### Configurazione
*Parola Chiave nel File :* `lanes_propose`

*Parametri :* un dizionario con chiavi i nomi delle propose.
A ogni propose è associato un dizionario così definito :
+ `source` : contiene una funzione che restituisce i dati su cui eseguire poi la funzione generatrice della distribuzione.
Questa funzione può essere definita in qualunque modo ma deve:
    1. accettare i parametri kwargs: information, constraint, distribution
    2. restituire un dataframe
+ `distribution` : definisce come ricavare una distribuzione dal dataframe che source restituisce. 
Può essere:
    + una lista di due stringhe rappresentati le colonne che deve avere la distribuzione
    + un dizionario
+ `info_key` : opzionale, se vuoto la chiave delle info è la stessa della chiave della distribuzione, altrimenti indica la PolEnt cui associare le informazioni
+ `info` : una lista di stringhe rappresentanti le colonne del dataframe contenenti informazioni da prelevare

Configurazione dizionario di `distribution`:
+ `key` : la colonna cui associare i seggi
+ `selector` : viene riconosciuto da `parse_row_selector_take` o
`parse_row_selector_value`
+ `seats` : può essere
    + `un_intero` : i candidati validi riceveranno lo stesso numero di seggi
    + `stringa_nome_colonna` : ogni candidato riceverà il numero di seggi associato alla colonna

*Risultato :* i valori restituiti sono:
+ una distribuzione
+ un dizionario contenente le informazioni richieste


---
## Totals
#### Funzionalità
Questa metaclasse mette a disposizione un sistema per la definizione operazioni su dataframe.

*Parola Chiave nel File :* `totals` e `totals_support`

La differenza tra le due parole chiavi risiede nella modalità di chiamata della funzione :
+ le funzioni `totals` hanno questa modalità di chiamata :
`self.totals(nome_funzione, *sbarramenti, **kwargs)`
+ invece `totals_support` utilizzano una sintassi differente : `self.nome_funzione(**kwargs)`

Oltre alla modalità di chiamata, le funzioni `totals` mettono a disposizioni il filtraggio dei dati sulla base di `*sbarramenti`.
Si veda la documentazione di `totFilter` per dettagli sul filtraggio.

*Parametri :* entrambe si compongono di un dizionario dove le chiavi sono `nome_funzione` e i valori sono dei dizionari con la seguente configurazione :
+ `type` : uno tra
    + `aggregate`
    + `transform`
    + `combination`
+ `rename` : un dizionario stringa-stringa con lo stesso comportamento di `rename` in `source`
+ `columns` : una lista di stringhe, si comporta come `rename` in `source`


Solo per `aggregate` e `transform` :
+ `source`: la source da chiamare per ricevere il dataframe di input. 
Qui è dove `**kwargs` e `*sbarramenti` vengono inoltrati.

Solo per `aggregate` :
+ `keys` : una lista di stringhe che indica quali colonne costituiscono la chiave
+ `ops` : un dizionario `nome_colonna : nome_op`, dove `nome_op` è :
    + `mean` : per la media aritmetica
    + `median` : per la mediana
    + `sum` : per la somma
    + `prod` : per il prodotto
    + o il nome di una funzione in commons

Solo per `combination` :
+ `function` : una stringa che indica la funzione da chiamare, avente i seguenti parametri:
    + un dataframe passato posizionalmente
    + un numero arbitrario di argomenti posizionali
    + un numero arbitrario di argomenti passati per chiave
+ `merge_keys` : le chiavi da usare per combinare i vari dataframe
+ `keys` : le chiavi da usare per dividere il dataframe combinato
+ `args` : una lista di:
    + stringa o intero o booleano: uno scalare
    + dizionario contenente le chiavi:
        + `type` : `series`, `dataframe` o `scalar`
        + `source`

**Nota su combination :** `combination` opera facendo il merge su `merge_keys` di tutti i dataframe e facendo groupby sul risultato usando `keys`. Per ogni gruppo risultante sarà chiamata la funzione
passando :
+ la slice di dataframe corrispondente
+ tutti i parametri `scalar`
+ per ogni `series` la linea corrispondente alla chiave del gruppo trattandola come un dizionario passato per kwargs.  

Una `series` è un oggetto di tipo dataframe con almeno le colonne `keys`, dove per ogni combinazione di `keys` c'è una e una sola linea.

Solo per `transform` :
+ `ops` : una lista di dizionari, a seconda del valore associato alla chiave `type` verrà trattato come:
    + transform column : applica un'operazione a tutti gli elementi di una data colonna, sovrascrivendola o creando una nuova colonna
    + transform line : chiama per ogni linea la funzione usando la linea come dizionario di `**kwargs`
    + transform dataframe: applica la funzione a tutto il dataframe

Le operazioni vengono eseguite in sequenza

Transform ops:
+ `column` :
    + `column` : la colonna da modificare
    + `column_type` : opzionale, se specificato converte le celle nel tipo dato (si veda `type` in external)
    + `replace_name` : opzionale, di default uguale a `column`, indica il nome della colonna generata
    + `source` : la funzione da chiamare fornendo come parametro la cella
+ `line` :
    + `source` : la funzione da chiamare fornendo come kwargs il dizionario equivalente alla linea
    + `column_name` : che nome assegnare alla colonna risultante
+ `dataframe` :
    + `source`: la funzione cui passare il dataframe

---

## Candidate
#### Funzionalità
Questa classe definisce le due funzioni necessarie per un candidato:
1. ricevere proposte di seggi dove si è stati eletti (e eventuali informazioni aggiuntive)
2. dove ci siano opportunità multiple il candidato deve scegliere quale accettare e quali rifiutare

#### Configurazione
*Parola Chiave nel File :* `candidate`

*Parametri :* un dizionario con la seguente configurazione :
+ `info_vars` : lista di variabili della classe Candidato che saranno aggiunte alle informazioni restituite quando un candidato viene eletto
+ `criteria` : può essere:
    + `first` : per indicare la prima proposta ricevuta
    + una lista di stringhe, le proposte vengono ordinate in base ai valori delle informazioni aggiuntive
    + il nome di una funzione
