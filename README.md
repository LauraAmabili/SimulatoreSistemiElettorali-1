# Simulatore di sistemi elettorali

Framework per l'elaborazione di sistemi elettorali

## Modo d'uso

Creare una cartella in Electoral Laws/nome_legge con la seguente struttura:
+ Data
+ Instances
+ Classes

si vedano Docs/ConfigurationDoc.md e Docs/Report.md per informazioni su cosa vada inserito
nelle cartelle

Eseguire in questa cartella:

```shell script
python -m src /path/to/folder_nome_legge
```

o in una console python:

```python
import src
src.run_simulation("/path/to/folder")
```

## Esempio

`ExampleDeliveri` contiene la configurazione per simulare le elezioni europee in Italia
del 2019 