# Coalizione.py
Il file Coalizione.py è il file di configurazione dell'entità Coalizione.

L'entità coalizione viene prima creata attraverso una mini configurazione con una stringa formattata yaml :

```yaml
metaclasses:
  - logger
  - subclass

subclass:
    - PolEnt
```

Questa esplicita il fatto che Partito è un'entità politica.

---
## Filter
Le entità politiche hanno un'importante funzione, quella di filtraggio.
Questa funzione ci consente d'introdurre le soglie di sbarramento e attraverso il parametro 'sbarramenti' e 'district' possiamo decidere come comportarci nelle varie situazioni.

Intestazione del filtro :
```python
def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs)
```

### Filtri Implementati
Per il Porcellum le coalizioni necessitavano di un solo tipo di filtro.

- **Filtro Nazionale** : in questa parte viene controllato se la coalizione ha superato la soglia di sbarramento nazionale del 10% del totale dei numeri elettorali nazionali.

---
## Partiti Spettanti Seggi
Questa funzione deve stabilire quali partiti all'interno di una determinata coalizione posso prendere seggi.
Essi vengono scelti sulla base di sbarramenti interni alla coalizione e sbarramenti regionali.

Nello specifico i partiti facenti parte di una coalzione prendono dei seggi di essa solo se :
- hanno superato lo sbarramento del 2% rispetto al totale dei numeri elettorali nazionali
- è il miglior perdente all'interno della coalizione, ovvero è il partito che si è avvicinato di più al superamento dello sbarramento del 2%, senza però superarlo
- hanno preso almeno il 20% dei voti regionali, questo sbarramento è da considerare solo nel caso di partiti che si sono presentati unicamente nelle regioni del Trentino Alto-Adige o Friuli-Venezia Giulia

