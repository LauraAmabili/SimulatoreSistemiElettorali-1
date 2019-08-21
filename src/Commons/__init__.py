import os, pkgutil, importlib, sys, inspect

for (_, name, _) in pkgutil.iter_modules([os.path.dirname(__file__)]):
    """
    Adattato da https://www.bnmetrics.com/blog/dynamic-import-in-python3
    Al momento dell'import di Metaclasses importa in automatico tutte le classe e funzioni contenute nei file
    """
    imported_module = importlib.import_module('.' + name, package='src.Commons')

    class_name = list(filter(lambda x: x[:2]!="__", dir(imported_module)))

    for i in class_name:
        oggetto = getattr(imported_module, i)
        if inspect.isclass(oggetto) or inspect.isfunction(oggetto):
            print(oggetto.__name__)
            setattr(sys.modules[__name__], oggetto.__name__, oggetto)

del i, oggetto, class_name, imported_module, name, os, pkgutil, importlib, sys, _, inspect  # Per evitare confusione nel
                                                                                            # dir(Metaclasses)