A simple python package to make reading csv files easier.
This package uses the built-in `csv` module in the backend
but produces a dict object with the csv file's column headings
as keys and the column's data as a list for easy manipulation.

If you are familier with the `pandas.read_csv` function. This returns
something like that.

*Usage*
------------------
```python
>>>from icsv.icsv import reader
>>>df = reader.read('path/to/csv')
>>>df.keys()
dict_keys(['key1','key2','key3'])
>>>df['key1']
[1,2,3,4,5]
>>>df['key1'][1] = 7
>>>df['key1']
[1,7,3,4,5]
```
Quite simple really and intentionally so.
Basically, after using the `read` command, you have a normal
python dictionery, which means everything you can do with dicts
you can do with the result of `read`. And everything you can do
with lists, you can do with the result of df[key]
