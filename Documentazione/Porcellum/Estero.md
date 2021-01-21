# Estero.yaml
Il file Estero.yaml è il file di configurazione dell'entità Estero.

In questo file configureremo gli attributi che l'Estero deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere l'Estero

```yaml
external:
  seggi:
    init: True
    type: int
  circoscrizioni_estere:
    init: True
```
Abbiamo specificato il fatto che Estero ha gli attributi :
- seggi : di tipo intero che deve essere inizializzato
- circoscrizioni_estere : deve essere inizializzato

I valori che questi due parametri prenderanno possono essere trovati al file [Instances/Estero.yaml]

Nello yaml ci riferiamo a questi attributi con la sintassi self.get_nomeAttributo :

```yaml
source:
    type: fun
    name: self.get_seggi
```

---
## Subdivisions
Qui definiamo da quali sottodivisioni l'Estero è composto.
Serve inoltre per poter chiamare delle funzioni della sottodivisione stessa.

```yaml
subdivisions:
  circoscrizioni_estere:
    type: Circoscrizione_Estera
    functions:
      - name: liste
        source:
          totals: liste
```

Abbiamo specificato che l'Estero è suddiviso sulla base dell'attributo "circoscrizioni_estere" il quale sarà di tipo Circoscrizione_Estera, vedere la configurazione al file [Classes/Circoscrizione_Estera.yaml].

Abbiamo inoltre esposto le funzioni di circoscrizioni_estere:
- liste : che andrà a prendere il totals liste in Circoscrizione_Estera.yaml

Nello yaml ci riferiamo a queste funzioni possono essere con la sintassi self.subs_nomeSubdivision_nomeFunzione :

```yaml
source:
    type: fun
    name: self.subs_circoscrizioni_estere_liste
```

---
## Lane
Qui definiamo quali lanes ha l'entità Estero, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  estero:
    node_type: head
    order_number: 1
    sub_level: Circoscrizione_Estera
    info_name: Estero
    first_input: liste
    operations:
      - collect_type: liste
        ideal_distribution: $
        corrector: Commons.correct_porcellum_estero
```

L'entità Estero avrà un lane con nome 'estero' così configurata :
- sarà di tipo head
- avrà priorità 1
- la lane di livello inferiore la si trova in [Classes/Circoscrizione_Estera.yaml]
- il nome della lane è Estero
- la distribuzione iniziale verrà data dalla lane_propose liste
- una volta eseguita la liste bisogna fare le seguenti operazioni
    - chiamare la lane_propose liste delle circoscrizioni_estere passando l'ultima distribuzione generata e correggere la distribuzione restituita con la funzione correct_porcellum_estero

---
## Lane_Propose
Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.

```yaml
lanes_propose:
  liste:
    source:
      type: fun
      name: self.estero
    distribution:
      - Lista
      - Seggi
    info:
      - Voti
```

La proposta 'liste' ha questa configurazine :
- chiamerà la funzione estero (vedere totals_support per chiarimenti)
- la distribuzione ritornata avrà le colonne Lista, Seggi (in questo ordine)
- info avrà solo il campo Voti

---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: fun
      name: self.subs_circoscrizioni_estere_liste
    columns:
        - Lista
        - Voti
    keys:
      - Lista
    ops:
      Voti: sum
```

Il totals 'liste' ha questa configurazine :
- è di tipo aggregazione
- la sua input di dati è la funzione self.subs_circoscrizioni_estere_liste (vedere external per chiarimenti)
- ritorna un dataframe con le colonne Lista, Voti
- aggrega i dati sulle chiavi Lista
- sui dati aggregati esegue l'operazione sum sul campo Voti

---
## Totals_Support
Qui definiamo delle funzione totals di supporto sulle quali avviene anche il filtraggio dei dati.

```yaml
totals_support:
  estero:
    source:
      totals: liste
      args:
        - estero
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.distrib_porcellum_estero
          kwargs:
            seats:
              source:
                type: fun
                name: self.get_seggi
```

Il totals_support 'estero' ha questa configurazione :
- è di tipo trasformazione
- il parametro 'data' della funzione che verrà chiamata avrà come sorgente il totals 'liste' e prenderà come valore di filtraggio 'estero'
- la trasformazione è su un dataframe
- la funzione da chiamare è 'distrib_porcellum_estero' e le devono essere passati questi ulteriori parametri
    - seats i cui dati vengono presi dalla funzione self.get_seggi

---









[Instances/Estero.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Instances/Estero.yaml>
[Classes/Circoscrizione_Estera.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Classes/Circoscrizione_Estera.yaml>