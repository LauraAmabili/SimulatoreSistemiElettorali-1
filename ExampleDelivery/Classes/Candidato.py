import yaml

conf = """
metaclasses:
    - logger
    - PolEnt
    - candidate

sub_of:
    - party
candidate:
    criteria: first
    info_vars:
        - party
"""

conf = yaml.safe_load(conf)

metas_p = list(map(eval, conf.pop("metaclasses")))
metas_p.append(cleanup)
metas_p
comb_p = type("combPol", tuple(metas_p), {})


class Candidato(metaclass=comb_p, **conf):
    pass
