import os, pkgutil, importlib, sys

for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    """
    Adattato da https://www.bnmetrics.com/blog/dynamic-import-in-python3
    Al momento dell'import di Metaclasses importa in automatico tutte le metaclassi contenute nei file
    """
    imported_module = importlib.import_module('.' + name, package='src.Metaclasses')

    class_name = list(filter(lambda x: x[:2]!="__", dir(imported_module)))

    for i in class_name:
        classe = getattr(imported_module, i)
        if issubclass(classe, type):
            print(classe.__name__)
            setattr(sys.modules[__name__], classe.__name__, classe)

del i, classe, class_name, imported_module, name, os, pkgutil, importlib, sys, _    # Per evitare confusione nel
                                                                                    # dir(Metaclasses)