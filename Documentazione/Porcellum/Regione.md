# Regione.yaml
Il file Regione.yaml è il file di configurazione dell'entità Regione.

In questo file configureremo gli attributi che la Regione deve avere, le sue sottodivisioni, le sue lanes e la sue funzioni di filtraggio, aggregazione e trasformazione.

## External
Qui definiamo quali parametri deve avere la Regione

```yaml
external:
  voti_regionali:
      - REGIONE -> Regione
      - COALIZIONE -> Coalizione
      - LISTA -> Lista
      - VOTI_LISTA -> Voti
  voti_liste:
    columns:
      - COALIZIONE -> Coalizione
      - LISTA -> Lista
      - VOTI_LISTA -> Voti
  voti_coalizioni:
    columns:
      - COALIZIONE -> Coalizione
      - VOTI_LISTA -> Voti
```
Abbiamo specificato il fatto che Nazione ha gli attributi :
- voti_regionali : restituisce i dati in dataframe in colonne Regione, Coalizione, Lista, Voti prendendo i dati da [Data/Regione/voti_regionali.csv]
- voti_liste : restituisce i dati in dataframe in colonne Coalizione, Lista, Voti prendendo i dati da [Data/Regione/voti_liste.csv]
- voti_coalizioni : restituisce i dati in dataframe in colonne Coalizione, Voti prendendo i dati da [Data/Regione/voti_coalizioni.csv]

---



[Data/Regione/voti_regionali.csv]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Data/Regione/voti_regionali.csv>
[Data/Regione/voti_liste.csv]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Data/Regione/voti_liste.csv>
[Data/Regione/voti_coalizioni.csv]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Data/Regione/voti_coalizioni.csv>