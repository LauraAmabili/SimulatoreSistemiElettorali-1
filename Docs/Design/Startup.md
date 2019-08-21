The module is called and provided, via command line argument the location of the configuration files. (using argparse
 to provide builtin documentation)

It will load Metaclasses and Commons, then proceed to look for a Metaclasses and Commons folder in the provided path
 and load the relevant metaclasses and common files (combination of os.walk, importlib spec_from_file_location
 , module_from_spec and loader.exec_module)

It will then add these to a particular dictionary. Obtained by the combination of standard and provided (if for
 example a metaclass has the same name as one in the standard library the new one takes precedence but a warning
  should be generated)

Once the software library is built the process will look for all files with extension `.cdf` (Class Definition File
) and iterate over them as explained in Configs#Class_Configuration

The next step is looking for `.idf` (Instance definition) files, if the file name is the name of a class defined in
 the previous step then it is to be assumed that the file (a YAML document) is a list and the class in question
  defaults to the class as found in the name. Otherwise the file is interpreted as a dictionary `"class name":"list"`

Finally the file will look for `.csv` files (to be loaded with UTF-8 encoding) whose names identify the class into
 which it will feed data. They will be read by pandas, a groupby on the first column will provide the instance
  identifier.
  
Once this process is completed the loader will call the `Simulator` module, providing the `Hub` object