# Circoscrizione_Estera.yaml
Il file Circoscrizione_Estera.yaml è il file di configurazione dell'entità Circoscrizione_Estera.

In questo file configureremo gli attributi che la Circoscrizione_Estera deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere la Circoscrizione_Estera

```yaml
external:
  voti_estero:
    columns:
      - Lista
      - Voti
  nome:
    init: True
  numero_seggi:
    init: True
```
Abbiamo specificato il fatto che Circoscrizione_Estera ha gli attributi :
- numero_seggi : che deve essere inizializzato
- nome : che deve essere inizializzato
- voti_estero : avendo il campo columns capiamo che questo attributo prende dei dati dal file con lo stesso nome della funzione, quindi [Data/Circoscrizione_Estera/voti_estero.csv]

I valori che questi due parametri prenderanno possono essere trovati al file [Instances/Circoscrizione_Estera.yaml]

Nello yaml ci riferiamo a questi attributi con la sintassi self.get_nomeAttributo :

```yaml
source:
    type: fun
    name: self.get_numero_seggi
```

---
## Lane
Qui definiamo quali lanes ha l'entità Circoscrizione_Estera, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  estero:
    node_type: tail
    info_name: Circoscrizione_Estera
```

L'entità Circoscrizione_Estera avrà un lane con nome 'estero' così configurata :
- sarà di tipo tail
- il nome della lane è Circoscrizione_Estera

---
## Lane_Propose
Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.

```yaml
lanes_propose:
  liste:
    source:
      type: fun
      name: self.estero
      rename:
        Votes: Voti
        Seats: Seggi
    distribution:
      - Lista
      - Seggi
    info:
      - Voti
      - Remainder
```

La proposta 'liste' ha questa configurazine :
- chiamerà la funzione estero (vedere totals_support per chiarimenti)
- la distribuzione ritornata avrà le colonne Lista, Seggi (in questo ordine)
- info avrà i campi Voti e Remainder

---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: transform
    source:
      type: att
      name: self.voti_estero
    ops:
      - type: dataframe
        source:
          type: fun
          name: commons.fill_column
          kwargs:
            column: 'Circoscrizione'
            column_val:
              source:
                type: att
                name: self.name
```

Il totals 'liste' ha questa configurazine :
- è di tipo transform
- la sua input di dati è l'attributo self.voti_estero (vedere external per chiarimenti)
- ritorna un dataframe con le colonne Partito, Coalizione, Voti
- la trasformazione è su un dataframe
- la funzione da chiamare è 'commons.fill_column' e le devono essere passati questi ulteriori parametri
    - 'Circoscrizione' ovvero la colonna da aggiungere al dataframe passato
    - il valore con cui riempire la colonna nel dataframe, in questo caso prendiamo il valore dall'attributo name

---
## Totals_Support
Qui definiamo delle funzione totals di supporto sulle quali avviene anche il filtraggio dei dati.

```yaml
totals_support:
  estero:
    type: transform
    source:
      type: att
      name: self.voti_estero
      rename:
        Voti: Votes
    ops:
      - type: dataframe
        source:
          type: fun
          name: commons.hondt
          kwargs:
            seats:
              source:
                type: fun
                name: self.get_numero_seggi
```

Il totals_support 'estero' ha questa configurazione :
- è di tipo trasformazione
- il parametro 'data' della funzione che verrà chiamata avrà come sorgente l'attributo self.voti_estero (vedere external per chiarimenti)
- la trasformazione è su un dataframe
- la funzione da chiamare è 'commons.hondt' e le devono essere passati questi ulteriori parametri
    - seats i cui dati vengono presi dalla funzione self.get_numero_seggi

---







[Data/Circoscrizione_Estera/voti_estero.csv]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/tree/master/Porcellum/Data/Circoscrizione_Estera>
[Instances/Circoscrizione_Estera.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Instances/Circoscrizione_Estera.yaml>