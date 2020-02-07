# Lane head

Parte da lane_head chiamando:

`head.lane_exec(lane_name)`

La lane head quindi si genera una distribuzione ideale chiamando:

`self.propose(ideale)`

Poi iniziano le operazioni, ogni operazione riceve in ingresso:
+ variabili locali
+ info_specifiche ai sottolivelli
+ info comuni
+ distribuzione ideale

e restituisce:
+ info specificiche ai sottolivelli (nuove, generate dalle propose sotto e da correct)
+ info generali (nuove, generate dalla ideale)
+ distribuzione

# Operazioni

Ogni operazione viene chiamata come:

```
operation(locs, 
          specific_infos: Dict[str, Dict[str, Dict[str, obj]]], 
          *general_infos: List[Dict[str, Dict[str, obj], 
          distribution: Union[pd.Dataframe, Dict[str, pd.DataFrame]])`
```

Prima di tutto genero una nuova distribuzione ideale se necessario

Poi chiamo le propose ai livelli inferiori fornendo:

+ distribuzione ideale
+ Le info locali a quella circoscrizione se esistono
+ Le info generali
+ Il constraint
+ la distribuzione attuale

`subdiv.propose(nome, local_info, *generic_info, constraint, distribution)`

Il risultato sarà nella forma `distribution, local_info`

Raccolgo tutti questi risultati e chiamo il corrector che mi restituisce la nuova distribuzione,
nuove informazioni locali ad ogni sottolivello, nuove informazioni generali

A questo punto aggrego tutte le informazioni locali e generali e passo all'operazione successiva
con queste informazioni

## Prima di chiamare

Prima di chiamare la funzione operation**s** creo un dizionario che rappresenta le informazioni
relative al distretto corrente, queste 


### Sulle informazioni

#### Locali:

**Generate** da propose nei sottolivelli e da correct

Le accumulo facendo il merge dei dizionari ogni volta che viene modificato qualcosa

C'è un solo dizionario con tutte le informazioni locali, quando passo all'exec_lane del livello
inferiore il sottodizionario specifico diventa l'elemento in testa a generic_info

#### Generali:

**Generate** da ideal e da correct ma anche ricevute dai livelli superiori

Non devo mai andare a toccare un dizionario generato a un livello superiore

Alle singole operazioni devo passare una lista di informazioni generiche e un dizionario di info
locali, **se prima della prima operazione aggiungo un dizionario vuoto** in testa allora posso
assumere che il primo elemento sia locale e modificarlo all'interno delle operazioni



# Lane node

Una volta effettuate le operazioni in lane_head o in un lane_node superiore mi ritrovo con:

1. Una distribuzione composta (dizionario di distribuzioni)
2. Una lista di informazioni comune, elementi con indici più bassi più recenti, questa lista
contiene sia informazioni precedenti che nuove
3. Un dizionario di informazioni specifiche

Procedo quindi a iterare sulle chiavi del dizionario di distribuzioni, e chiamo sul livello
inferiore:

`lane_node.exec_lane(lane_name, info_specifiche, *informazioni_comuni, 
distribution=distribution)`

Da questo momento le operazioni sono uguali a lane head eccetto che non genero nessuna 
distribuzione prima di entrare nelle operazioni

# Lane tail

Lane tail riceve gli stessi input di lane_node ma non esegue alcuna operazione.

Crea invece un dizionario locale, nel quale concatena tutte le informazioni, dalla meno recente 
alla più recente (cosicché, dovessero esserci conflitti il più recente avrebbe la precedenza)

Per ogni chiave del dizionario di informazioni trova la `PolEnt` corrispondente e chiama:

`PolEnt.log(**info)` su di essa

Una volta fatto ciò itera sulle righe del dataframe distribuzione e aggiunge alla lista che verrà
restituita una tupla: `(nome_lane, self, contenuto_prima_colonna, contenuto_seconda_colonna)`

La prima colonna sarà una stringa che fa' riferimento a PolEnt, la seconda un intero che indica i
seggi da eleggere nella circoscrizione `self`


















