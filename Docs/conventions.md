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
+ transform: Take the data from a given function of the instance and apply a transformation
+ combine: Take the data from two or more sources and combine/transform the results

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
def groupbyFunc(df):
pass

def totals_coalizione(self, sbarramento=None):
	d_or = {'attrName':'uninominali',
		'subFuncKwargs':{'tipo':'lista'},
		'renamesPreAgg':{'votiLista':'voti'},
		'renamesPostAgg':{'voti':'votiCoalizione'},
		'groupby':grouper_func,
		'agg':{'voti':'sum','col':func},
		}
	
	d = d_or.copy()
	d['subFuncKwargs']['sbarramento'] = sbarramento

	listaSubs = getattr(self, d['attrName'])
	iterator = map(lambda s: self.Hub.getInstance(self.tipi_sub[d['attrName']], s)
				.totals(**d['subFuncKwargs']), listaSubs)
	df = pd.concat(iterator,ignore_index=True)
	df.rename(columns=d['renamesPreAgg'], inplace=True)
	grouped = d['groupby'](df)
	df = grouped.agg(d['agg'])
	df.rename(columns=d['renamesPostAgg'], inplace=True)
	return df
```

In order for this to work I must transform the aggregating part of the configuration manually and
obtain a callable function that takes a dataframe and returns a groupby

## Transform
This method takes a pre-existing function and applies a transformation on its result

**Is this necessary?***

## Combine
This method takes the outputs from multiple functions and combines it

The results should be dataframes but aren't necessarily treated as dataframes. Moreover grouping 
might still be necessary

For instance in the case of the party result in the Rosatellum system we have to combine the results
of the tally for each candidate with the votes for parties supporting the given candidate

We will therefore have two dataframes:
+ candidate: with columns [candidate, votes]
+ list_raw : with columns [candidate, list, votes]

We know that for the candidate dataframe the "candidate" column is a key, while for the list_raw 
dataframe the key is "list" and we will have to process lists with the same candidate in bulk

Moreover the function expects a dataframe and a scalar, not two dataframes (I plan on reusing the
function used for seat redistribution)

What I need is a way to specify:
1. Which subset of dataframes to use
2. The key to use for each dataframe. The keys might be different but their content must be the 
same
3. Which dataframes provide dataframes and which provide scalars
4. The function I'll use and the parameters it needs


```
totals lista: comb {
	scalar: votes @ #totals("candidate") ["candidate","votes"]
	votes -> votes_candidate
	index "candidate"

	frame : df @  #totals("raw_list") ["candidate","list", "votes"]
	"list" -> "party"
	"candidate" -> "candidato"

	key "candidato" #Common to all frames

	func commons.hondt {df, votes}
	"seats" -> "votes"
	"party" -> "list"
	"candidate" -> *
}
```

```python
from functools import reduce
def comb_ex():
	vars = dict()
	scalars = []
	frames = []
	
	#Ciclo for
	temp = self.totals("candidate")[["candidate","votes"]]
	temp.set_index('candidate', inplace=True) #perché è scalar
	cols = ["candidate", "votes"]
	cols.pop(cols.index('candidate')
	vars['votes']=pd.Series(temp.loc[:,cols[0]])
	scalars.append('votes')
	
	#
	temp = self.totals("raw_list")[["candidate","list","votes"]]
	temp.rename({'list':'party', 'candidate':'candidato')
	vars['df'] = temp.copy()
	frames.append('df')

	#ops
	
	#Crea un dizionario "df" -> ["colonne"]	

	common_series_keys = [...]
	if len(frames)==0:
		pass
	if len(frames)==1:
		complete_frame = vars[frames[0]]
	else:
		complete_frame = reduce(lambda l,r: pd.merge(l,r,on=["candidato"]), 
					map(lambda x: frames[x], frames))
	
	if len(frames)==0:
		aggrega: func(vars['first_arg'][chiave], ..., vars['nth_arg'][chiave])
	else:
		groups = complete_frame.groupby(['candidato'])
		lis_res = []
		for (c, df) in groups:
			lis_res.append(func(df[colonne['arg1']], ...)
			# creare gli args in un for per gestire gli scalari, poi passarli 
			# tramite args
			# Comunque quando nella config c'era il nome di un df allora
			# passo il sottodataframe con le colonne adatte (incluse quelle chiave)
			# Se si tratta di uno scalare invece uso la chiave per trovare il valore
			# corrispondente a quello del groupby e passo quel valore
		
		pd.concat(lis_res).reset_index(drop=True)
```

#























