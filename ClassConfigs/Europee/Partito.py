import yaml
conf = """
metaclasses:
  - PolEnt
  - totFilter
  - logger # aggiunge automaticamente una funzione log

filter: # l'input ha le seguenti informazioni:
        # distretto chiamato,
  eletto:
    source:
      # totals sul distretto di tipo Nazione sopra self
      # Come?
      # rebase: mi permette di cambiare il valore di self contenuto nelle variabili locali
      # rebase:
      #     ancestor: Nazione
      # Altri controlli:
      #   exclude:  # non effettual il filter sulla classe o sulla classe/tipo di totals
      #     - class: Circoscrizione
      #       type: liste
"""

conf = yaml.safe_load(conf)

metas = list(map(eval, conf.pop("metaclasses")))
comb = type("combined", tuple(metas), {})

class Partito(metaclass=comb, **conf):
    def eleggi(self, lane, district, seats):
        pass
