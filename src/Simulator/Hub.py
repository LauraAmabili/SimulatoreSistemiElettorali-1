"""
This file will create the class structure of a simulation, it will expose a class with a method 
which, upon being
called with the parsed configuration, will return the Hub object

The parsed configuration consists of:
    + List with one dictionary element per class to be created
    + All metaclasses strings are replaced by the actual metaclass
    + Other strings are interpreted as numbers where necessary
"""


class Hub:
    """
    This object will contain references to all classes created and other globally available values

    classes: Dictionary mapping the name to: the class, the class it derives from and the classes
    derived from it.

        Ex: "Lista":(Lista, ["Coalizione"], ["ListaRegionale"])

    """

    def __init__(self):
        self.classes = dict()

    def addClass(self, name, cls):
        self.classes[name] = (cls, dict())

    def getClass(self, name):
        return self.classes[name][0]

    def getInstances(self, class_name):
        return self.classes[class_name][1]

    def addRegister(self, registerName, register=None):
        """
        Adds a register to the Hub
        :param registerName:
        :param register:
        :return:
        :exception: Throws a KeyError if the register exists already
        """
        if register is None:
            register = dict()
        if hasattr(self, registerName):
            raise KeyError("Register already exists")
        else:
            setattr(self, registerName, register)

    def retrieveRegister(self, registerName):
        """
        Returns the reference to the register object so that the
        :param registerName:
        :return: The register object reference, you can modify the original object
        :exception: Throws a KeyError if the register doesn't exist
        """
        if hasattr(self, registerName):
            return getattr(self, registerName)
        else:
            raise KeyError("No such register")

    def getLaneOrder(self):
        pass


class HubBuilder:
    def __init__(self):
        pass

    @staticmethod
    def classBuilder(name, hub, bases, kwargs):
        """
        This function creates the class based on the given metaclasses
        :param name: The name of the class to be created
        :param hub: The hub used by the application
        :param bases: The metaclasses from  which it inherits
        :param kwargs: The parameters each metaclass needs to create the object
        :return: A class of type a temporary metaclass created by inheriting from all the bases
        """
        class cleanupMeta(type):
            def __new__(cls, *args, **ks):
                return super().__new__(cls, *args)

        bases.append(cleanupMeta)
        metaclass = type('combined', bases, {})
        return metaclass(name, (), {}, **kwargs)

    @staticmethod
    def buildHub(config, dict_metas, dict_commons):
        """
        This function takes the configuration (provided as a string-dictionary pairing) and creates
        the classes by calling classBuilder.
        It then adds the result to an Hub and returns it
        :param config: The dictionary obtained by merging all class definition files
        :return: An Hub object
        """
        retHub = Hub()
        for name, cls_conf in config.items:
            bases = []
            conf_f = dict()
            for meta_n, meta_conf in cls_conf.items:
                metaclass = dict_metas[meta_n]
                bases.append(metaclass)
                conf_f[meta_n] = metaclass.parse_conf(meta_conf, dict_commons)
            cls = HubBuilder.classBuilder(name, retHub, bases, conf_f)
            Hub.addClass(name, cls)

        return retHub
