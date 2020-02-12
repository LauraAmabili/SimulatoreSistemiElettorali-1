# Class definition

## Process overview
Class definition is achieved by means of yaml files, each class will have its own file whose name is the same name as 
the class it's defining

The top level is going to be a dictionary, one key will always be `metaclasses` which maps to a list of metaclass names:

```yaml
metaclasses:
    - first_metaclass
    - second_metaclass
    - ...
```

these metaclasses will be then added in that same order to create a combined metaclass

After this, but before beginning the creation of the class, the remaining configuration will be passed through each
metaclass' `config_parse` function, if such a function exists. This is to expand syntactic sugars such as totals':
`totals: tot_name`, which expands to:
```yaml
type: fun
name: self.totals
args:
    - tot_name
    - any other arg defined in the original snippet
```

After this the whole configuration is passed through the generic parsers, which are triggered by a specific keyword and 
substitute the dictionary mapped to the keyword with a python object

Once this step is complete the whole parsed configuration (save for `metaclasses`) is passed as kwargs to the combined 
metaclass:

`combined("File_name", (), {}, **conf)`

## Generic snippets
Some configuration snippets are not metaclass specific and are parsed by an independent function

### Source
This parser handles configurations of form:

```yaml
source:
    type: (fun|att|kwarg)
    name: str
    args:
      - (literal|source:dict)
    kwargs:
        name: (literal|source:dict)
    store: str
    rename:
        str: str
    columns:
        - str (-> str)?
    options:
        - NoForward
    
```

The value mapped to store can be:
+ None
+ A simple string, which will store the result in the locals dictionary
+ A string beginning with '#' which will take the value named 'self' in locals and store the result in the attribute
+ A string beginning with '$' and with a dot in the middle which stores the value in a dictionary

The result is `source` mapping to a function which accepts a local namespace dictionary, a variadic number of positional
and keyword arguments, computes a value, stores it as instructed and then returns the value itself

The options keyword, mapping to a list, allows advanced behaviour, **NoForward** means that the extra arguments will not
be passed to the actual functions

Columns assumes the result is a dataframe and shows in the result only the columns mentioned, in the order mentioned.

The  `-> str` part means that the column will be renamed

Rename also assumes that the result is a dataframe and renames the columns, where columns and rename conflict rename
is applied

## External
This metaclass provides the interface between the program and the real world. It allows to define attributes of a class
that are either filled in at instantiation, through keyword arguments, or at runtime, through specific functions

Its configuration is of the form:

```yaml
name_var:
    init: True
    targets:
        - columns: 
              - str (-> str)?
          name: str


name_var_2:
    type: str
    name: str
    columns:
        - str (-> str)?
```

The first level key determines the name of the setter, which will be of the form: object.give_name_var

If `init` is true then I'll have to require the variable value at instantiation

If `targets` exists as a key then more than an output will be derived from a single input, this could be the case for
dataframes containing many columns

`name` is a string which determines the name of the getter, it's mandatory only under `targets`

`columns` is parsed as in sources

`type` means that the value provided is of the given type, the getter will convert it before returning, the only types
allowed are user defined ones (as in classes defined in the program), int or float

## Superdivisions


## Totals

## Lane

## Elector

## Filter

## Logger

## Candidate























