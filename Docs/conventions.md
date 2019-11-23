# Function call

```
var res: func commons.func_name {arg1, "arg2", key1 -> #val1}
```

becomes:

```
func_name = getattr(commons, "func_name")
res = func(eval("arg1"), "arg2", **{"key1":getattr(self, "val1")}
```

and in yaml:

```
res:
  type: var
  origin:
    type: func
    name: commons.Function
    args: 
      - type: variable
        name: arg1
      - arg2
    kwargs:
      key1:
        type: attribute
        name: arg3
```

# Totals:
I start the definition with `totals name` where name will be the case

After I can have the following cases:
+ subs: Aggregate the results from all subdivisions of a certain type
+ func: Take the data from a given function of the instance and apply a transformation
+ comb: Take the data from two or more sources and combine/transform the results

## Subs
Subs is the simplest, I have to specify:
+ the list on which to apply
+ the function to call
+ the aggregation method

The expression `subs.{list}.{func}` translates to concatenating the results of the given function
when mapped over the list. 

**Assumption: the functions result in homogeneous dataframes**

I can also provide extra arguments by wrapping them in square brackets `[tipo -> "coalizione"]`

Finally inbetween the curly brackets I will provide the rules for the aggregation which will 
consist of:
1. Key
2. Function

The key can be either `key val` or `keys val1 val2`

`val` can be a simple string matching `[a-zA-0-9]+` or it can match:
+ `[a-zA-0-9]+\.[a-zA-0-9]+`: which will access a parameter on the column
+ `[a-zA-0-9]+\.[a-zA-0-9]+\(DICT\)` which will call the function on the elements of the column and
pass the DICT (string -> string) as kwargs

In both cases the column will be renamed accordingly

The aggregation function will be:
+ A string
+ A dictionary with values strings

If it's a string then it should start with `commons.` or be directly interpretable by pandas

If it's a dictionary the same constraint holds for the individual values

Optionally, after before and after the Function definition I can put manipulations of the form:

`columnName -> newName` to rename a column, or `columnName -> *` to delete it

So:
```
totals coalizione: subs.uninominali.totals [tipo -> "lista"] {
	key lista.coalizione
	votiLista -> voti
	{"voti":"sum",'col':commons.func}
	voti -> votiCoalizione
}
```

becomes:
```python
def groupbyFunc(

def totals_coalizione(self, sbarramento=None):
	d_or = {'attrName':'uninominali',
		'subFuncKwargs':{'tipo':'lista'},
		'renamesPreAgg':{'votiLista':'voti'},
		'renamesPostAgg':{'voti':'votiCoalizione'},
		'groupby':
		'agg':{'voti':'sum','col':func},
		}
	
	d = d_or.copy()
	d['subFuncKwargs']['sbarramento'] = sbarramento

	listaSubs = getattr(self, d['attrName'])
	iterator = map(lambda s: self.Hub.getInstance(self.tipi_sub[d['attrName']], s)
				.totals(**d['subFuncKwargs']), listaSubs)
	df = pd.concat(iterator,ignore_index=True)
	df.rename(columns=d['renamesPreAgg'], inplace=True)
	
	
	
	
```










