# Circoscrizione.yaml
Il file Circoscrizione.yaml è il file di configurazione dell'entità Circoscrizione.

In questo file configureremo gli attributi che la Circoscrizione deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere la Circoscrizione

```yaml
external:
  regioni:
    init: True
  numero_seggi:
    init: True
```
Abbiamo specificato il fatto che Circoscrizione ha gli attributi :
- numero_seggi : deve essere inizializzato
- regioni : deve essere inizializzato

I valori che questi due parametri prenderanno possono essere trovati al file [Instances/Circoscrizione.yaml]

Nello yaml ci riferiamo a questi attributi con la sintassi self.get_nomeAttributo :

```yaml
source:
    type: fun
    name: self.get_numero_seggi
```

---
## Subdivisions
Qui definiamo da quali sottodivisioni la Circoscrizione è composta.
Serve inoltre per poter chiamare delle funzioni della sottodivisione stessa.

```yaml
subdivisions:
  regioni:
    type: Regione
    functions:
      - name: liste
        source:
          type: fun
          name: self.get_voti_liste
      - name: coalizioni
        source:
          type: fun
          name: self.get_voti_coalizioni
      - name: regioniListe
        source:
          type: fun
          name: self.get_voti_regionali
```

Abbiamo specificato che la Circoscrizione è suddivisa sulla base dell'attributo "regioni" il quale sarà di tipo Regione, vedere la configurazione al file [Classes/Regione.yaml].

Abbiamo inoltre esposto le funzioni di regioni:
- liste : che andrà a prendere la funzione self.get_voti_liste in Regione.yaml
- coalizioni : che andrà a prendere la funzione self.get_voti_coalizioni in Regione.yaml
- regioniListe : che andrà a prendere la funzione self.get_voti_regionali in Regione.yaml

Nello yaml ci riferiamo a queste funzioni con la sintassi self.subs_nomeSubdivision_nomeFunzione :

```yaml
source:
    type: fun
    name: self.subs_regioni_liste
```

---
## Lane
Qui definiamo quali lanes ha l'entità Circoscrizione, la priorità di ogni lane, il sottolivello e quali operazioni aggiuntive deve fare.

```yaml
lane:
  lista:
    node_type: tail
    info_name: Circoscrizione
```

L'entità Circoscrizione avrà un lane con nome 'lista' così configurata :
- sarà di tipo tail
- il nome della lane è Circoscrizione

---
## Lane_Propose

Qui definiamo quale funzione chiamare per generare la distribuzione, quali campi deve avere la distribuzione quando viene restituita e quali campi deve avere info quando viene restituito.

```yaml
lanes_propose:
  liste:
    source:
      type: fun
      name: commons.divisione_circoscrizionale_seggi
      kwargs:
        district_votes:
          source:
            totals: liste
        seggi:
          source:
            type: fun
            name: self.get_numero_seggi
    distribution:
      - Eleggibile
      - Seggi
      - Voti_Circ
      - Resto
      - Resto_Usato
    info:
      - Indice
```

La proposta 'liste' ha questa configurazine :
- chiamerà la funzione divisione_circoscrizionale_seggi che prende questi parametri :
    - district_votes il cui valore viene preso dal totals liste
    - seggi il cui valore viene preso dall'attributo della circoscrizione
- la distribuzione ritornata avrà le colonne Eleggibile, Seggi, Voti_Circ, Resto, Resto_Usato (in questo ordine)
- info avrà solo il campo Indice

---
## Totals
Qui definiamo delle funzioni di aggregazione, trasformazione e combinazioni di dati presi da dei dataframe pandas.

```yaml
totals:
  liste:
    type: aggregate
    source:
      type: fun
      name: self.subs_regioni_liste
      columns:
        - Lista -> Partito
        - Coalizione
        - Voti
    keys:
      - Partito
      - Coalizione
    ops:
      Voti: sum
```

Il totals 'liste' ha questa configurazine :
- è di tipo aggregazione
- la sua input di dati è la funzione self.subs_regioni_liste (vedere external per chiarimenti)
- ritorna un dataframe con le colonne Partito, Coalizione, Voti (la colonna Partito è ottenuta rinnominando Lista)
- aggrega i dati sulle chiavi Coalizione, Partito
- sui dati aggregati esegue l'operazione sum sul campo Voti

---












[Instances/Circoscrizione.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Instances/Circoscrizione.yaml>
[Classes/Regione.yaml]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Classes/Regione.yaml>