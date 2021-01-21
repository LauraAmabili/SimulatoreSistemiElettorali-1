# Valle_Aosta.yaml
Il file Valle_Aosta.yaml è il file di configurazione dell'entità Valle_Aosta.

In questo file configureremo gli attributi che la Valle_Aosta deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere la Valle_Aosta

```yaml
external:
  voti_valle_d_aosta:
    columns:
      - LISTA -> Partito
      - VOTI_LISTA -> Voti
```
Abbiamo specificato il fatto che Valle_Aosta ha gli attributi :
- voti_valle_d_aosta : avendo il campo columns capiamo che questo attributo prende dei dati dal file con lo stesso nome della funzione, quindi [Data/Circoscrizione_Estera/voti_estero.csv]

I valori che questi due parametri prenderanno possono essere trovati al file [Data/Valle_Aosta/voti_valle_d_aosta.csv]

Nello yaml ci riferiamo a questi attributi con la sintassi self.nomeAttributo :

```yaml
source:
    type: att
    name: self.voti_valle_d_aosta
```

---
## Lane
Qui definiamo quali lanes ha l'entità Valle_Aosta, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  valle_d_aosta:
    node_type: only
    order_number: 1
    first_input: None
    distribution: uninom
    info_name: Valle D'Aosta
```

L'entità Valle_Aosta avrà un lane con nome 'valle_d_aosta' così configurata :
- sarà di tipo only
- avrà priorità 1
- il nome della lane è Valle D'Aosta
- la distribuzione è data dalla lane_propose uninom

---
## Lane_Propose
Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.

```yaml
lanes_propose:
  uninom:
    source:
      type: fun
      name: self.valle_d_aosta
    distribution:
      - Partito
      - Seggi
    info:
      - Numero
```

La proposta 'uninom' ha questa configurazine :
- chiamerà la funzione self.valle_d_aosta (vedere totals_support per chiarimenti)
- la distribuzione ritornata avrà le colonne Partito, Seggi (in questo ordine)
- info avrà solo il campo Numero

---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: att
      name: self.voti_valle_d_aosta
    rename:
      LISTA: Partito
      VOTI_LISTA: Voti
    columns:
        - LISTA
        - VOTI_LISTA
    keys:
      - LISTA
    ops:
      VOTI_LISTA: sum
```

Il totals 'liste' ha questa configurazine :
- è di tipo aggregazione
- la sua input di dati è la funzione self.voti_valle_d_aosta (vedere external per chiarimenti)
- ritorna un dataframe con le colonne LISTA, VOTI_LISTA
- aggrega i dati sulle chiavi LISTA
- sui dati aggregati esegue l'operazione sum sul campo VOTI_LISTA
- le colonne LISTA, VOTI_LISTA del dataframe verranno rinnominate rispettivamente Partito, Voti

---
## Totals_Support
Qui definiamo delle funzione totals di supporto sulle quali avviene anche il filtraggio dei dati.

```yaml
totals_support:
  valle_d_aosta:
    source:
      totals: liste
    type: transform
    ops:
      - type: dataframe
        source:
          type: fun
          name: Commons.distrib_porcellum_aosta
```

Il totals_support 'valle_d_aosta' ha questa configurazione :
- è di tipo trasformazione
- il parametro 'data' della funzione che verrà chiamata avrà come sorgente il totals 'liste'
- la trasformazione è su un dataframe
- la funzione da chiamare è 'Commons.distrib_porcellum_aosta' alla quale non servono ulteriori ulteriori parametri

---



[Data/Valle_Aosta/voti_valle_d_aosta.csv]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Data/Valle_Aosta/voti_valle_d_aosta.csv>