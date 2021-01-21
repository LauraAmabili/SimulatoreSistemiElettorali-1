# Nazione.yaml
Il file Nazione.yaml è il file di configurazione dell'entità Nazione.

In questo file configureremo gli attributi che la Nazione deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere la Nazione

```yaml
external:
  seggi:
    init: True
    type: int
  circoscrizioni:
    init: True
```
Abbiamo specificato il fatto che Nazione ha gli attributi :
- seggi : di tipo intero che deve essere inizializzato
- circoscrizioni : deve essere inizializzato

I valori che questi due parametri prenderanno possono essere trovati al file [Instances/Nazione.yaml]

Nello yaml ci riferiamo a questi attributi con la sintassi self.get_nomeAttributo :

```yaml
source:
    type: fun
    name: self.get_seggi
```

---
## Subdivisions
Qui definiamo da quali sottodivisioni la Nazione è composta.
Serve inoltre per poter chiamare delle funzioni della sottodivisione stessa.

```yaml
subdivisions:
  circoscrizioni:
    type: Circoscrizione
    functions:
      - name: liste
        source:
          totals: liste
      - name: coalizioni
        source:
          totals: coalizioni
      - name: regioniListe
        source:
          totals: regioniListe
```

Abbiamo specificato che la Nazione è suddivisa sulla base dell'attributo "circoscrizioni" il quale sarà di tipo Circoscrizione, vedere la configurazione al file [Classes/Circoscrizione.yaml].

Abbiamo inoltre esposto le funzioni di circoscrizione:
- liste : che andrà a prendere il totals liste in Circoscrizione.yaml
- coalizioni : che andrà a prendere il totals coalizioni in Circoscrizione.yaml
- regioniListe : che andrà a prendere il totals regioniListe in Circoscrizione.yaml

Nello yaml ci riferiamo a queste funzioni possono essere con la sintassi self.subs_nomeSubdivision_nomeFunzione :

```yaml
source:
    type: fun
    name: self.subs_circoscrizioni_regioniListe
```

---
## Lane
Qui definiamo quali lanes ha l'entità Nazione, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  lista:
    node_type: head
    order_number: 1
    sub_level: Circoscrizione
    info_name: Nazione
    first_input: liste
    operations:
      - collect_type: liste
        ideal_distribution: $
        corrector: Commons.correct_porcellum
      - collect_type: partiti
        ideal_distribution: $
        corrector: Commons.correct_porcellum_partiti
```

L'entità Nazione avrà un lane con nome 'lista' così configurata :
- sarà di tipo head
- avrà priorità 1
- la lane di livello inferiore la si trova in [Classes/Circoscrizione.yaml]
- il nome della lane è Nazione
- la distribuzione iniziale verrà data dalla lane_propose liste
- una volta eseguita la liste bisogna fare le seguenti operazioni
    - chiamare la lane_propose liste delle circoscrizioni passando l'ultima distribuzione generata e correggere la distribuzione restituita con la funzione correct_porcellum
    - chiamare la lane_propose partiti delle circoscrizioni passando l'ultima distribuzione generata e correggere la distribuzione restituita con la funzione correct_porcellum_partiti

---
## Lane_Propose
Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.

```yaml
lanes_propose:
  liste:
    source:
      type: fun
      name: self.distribuisci_seggi
      rename:
        Votes: Voti
        Seats: Seggi
    distribution:
      - Partito
      - Seggi
      - Coalizione
    info:
      - Voti
```

La proposta 'liste' ha questa configurazine :
- chiamerà la funzione distribuisci_seggi (vedere totals_support per chiarimenti)
- la distribuzione ritornata avrà le colonne Partito, Seggi, Coalizione (in questo ordine)
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
      name: self.subs_circoscrizioni_liste
    columns:
        - Partito
        - Coalizione
        - Voti
    keys:
      - Coalizione
      - Partito
    ops:
      Voti: sum
```

Il totals 'liste' ha questa configurazine :
- è di tipo aggregazione
- la sua input di dati è la funzione self.subs_circoscrizioni_liste (vedere external per chiarimenti)
- ritorna un dataframe con le colonne Partito, Coalizione, Voti
- aggrega i dati sulle chiavi Coalizione, Partito
- sui dati aggregati esegue l'operazione sum sul campo Voti

---
## Totals_Support
Qui definiamo delle funzione totals di supporto sulle quali avviene anche il filtraggio dei dati.

```yaml
totals_support:
  distribuisci_seggi:
    source:
      totals: coalizioni
      args:
        - elette
      rename:
        Coalizione: Eleggibile
        Voti: Votes
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.distrib_porcellum
          kwargs:
            seats:
              source:
                type: fun
                name: self.get_seggi
            df_partiti_filtrato:
              source:
                totals: liste
                args:
                  - elette
                rename:
                  Partito: Eleggibile
                  Voti: Votes
            df_partiti_regioni:
              source:
                totals: regioniListe
                args:
                  - regione
                rename:
                  Partito: Eleggibile
                  Voti: Votes
            dividi_partiti:
              False
```

Il totals_support 'distribuisci_seggi' ha questa configurazione :
- è di tipo trasformazione
- il parametro 'data' della funzione che verrà chiamata avrà come sorgente il totals 'coalizioni' e prenderà come valore di filtraggio 'elette'
- la trasformazione è su un dataframe
- la funzione da chiamare è 'distrib_porcellum' e le devono essere passati questi ulteriori parametri
    - df_partiti_filtrato i cui dati vengono presi dal totals 'liste' con valore di filtraggio 'elette'
    - df_partiti_regioni i cui dati vengono presi dal totals 'regioniListe' con valore di filtraggio 'regione'
    - dividi_partiti un booleano con valore False

---






[Instances/Nazione.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali/blob/master/Porcellum/Instances/Nazione.yaml>
[Classes/Circoscrizione.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali/blob/master/Porcellum/Classes/Circoscrizione.yaml>