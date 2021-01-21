# Partito.py
Il file Partito.py è il file di configurazione dell'entità Partito.

L'entità partito viene prima creata attraverso una mini configurazione con una stringa formattata yaml :

```yaml
metaclasses:
    - logger
    - PolEnt
    - party

subclass:
    - PolEnt

sub_of:
    - coalition

party:
    info_vars:
        - coalition
```

Questa esplicita il fatto che Partito è un'entità politica e che sta sotto ad una 'coalition', ovvero una Coalizione. (vedere file di configurazione [Classes/Coalizione.py])

---
## Filter
Le entità politiche hanno un'importante funzione, quella di filtraggio.
Questa funzione ci consente di introdurre le soglie di sbarramento e attraverso il parametro 'sbarramenti' e 'district' possiamo decidere come comportarci nelle varie situazioni.

Intestazione del filtro :
```python
def filter(self, district, *, total, row, dataframe, sbarramenti, **kwargs)
```

### Filtri Implementati
Per il Porcellum era importante introdurre diverse filtri per i partiti a seconda dell'area di cui stiamo elaborando i numeri elettorali.

Ho suddiviso il filtro in tre parti :
- **Filtro Estero** : importante diversificare il filtro estero perchè, usato un sistema puramente proporzionale per i seggi esteri, bisogna solamente considerare lo sbarramento del 4% rispetto al totale delle cifre elettorali estere.
- **Filtro Nazionale** : in questa parte viene controllato se il partito fa parte di una coalizione che abbia superato la soglia di sbarramento delle coalizioni al 10%. <br> Nel caso non faccia parte di una coalizione, o la coalizione di cui fa parte non passa lo sbarramento, allora viene controllato se il singolo partito supera la soglia di sbarramento nazionale al 4% del totale dei numeri elettorali nazionali.
- **Filtro Regionale** : in questa parte viene controllato se il partito ha superato lo sbarramento regionale del 20% del totale dei numeri elettorali circoscrizionali ma solo per il Trentino-Alto Adige e Friuli-Venezia Giulia.







[Classes/Coalizione.py]:<https://github.com/LauraAmabili/SimulatoreSistemiElettorali-1/blob/master/Porcellum/Classes/Coalizione.py>