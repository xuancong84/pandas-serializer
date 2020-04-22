# pandas-serializer
A utility for text-based serialization and deserialization (i.e., save/load) of Python nested container objects (such as list, dict and set), containing Pandas DataFrame/Series and NumPy arrays/matrices, etc.
DataFrame/Series conformance behaviour is the same as pandas.DataFrame.to_csv() and pandas.read_csv() .

**Exported functions**:
- pandas_save(obj, fp_fn) : save object into the file/filename
- pandas_saves(obj) : save object into a string
- pandas_load(fp_fn) : load object from the file/filename
- pandas_loads(str) : load object from the string

**Internal functions**:
- Open(filename, mode) : smartly open normal or gzipped file, - for STDIN/STDOUT
- pandas_encode : recursively convert every non-convertible objects into specially-coded string
- pandas_decode : recursively restore every non-convertible objects from specially-coded string

The working principle is to first convert every non-convertible object (such as DataFrame/Series/types/modules) into a specially-coded string, then use Python repr() to convert the entire object in one go.
In addition, this powerful utility will also try to convert/restore other non-reverse-convertible Python objects such as types, modules, functions, etc. However, non-reverse-convertible Python object does not guarantee successful deserialization, so those data types should be avoided in general.

As shown in the built-in example, this utility can successfully serialize and deserialize the following super-complex nested data structure:

```python
[1, 3.4, 1.1+2.1j, np.nan, None, True, False, b'ab12', 'abc', int, float,
 pd.Series(), pd.DataFrame(), pd.DataFrame, type(pd.DataFrame), ['a', 1],
 lambda a,b,*args,x=0.5,y=-0.1: a**2+b+sum([*args])+x*y+1,
 {
  'a':1,
  'b':2,
  type:0,
  int:1,
  print:max,
  pd:np,
  0:pd.DataFrame(np.random.randint(0,256,[4,4]),
                 columns=['index a1', 'index a2', 'b', 'c'],
                 index=pd.date_range('2020-01-01', '2020-01-04')).set_index(['index a1', 'index a2'], append=True),
  1:pd.Series([1, 2.5, 3+1j, np.nan, 'abc'], index=pd.date_range('2020-01-01', '2020-01-05', tz='Asia/Singapore')),
  2:np.array([[1, 2.5, 'a'], [1+.5j, np.nan, 'b']]),
  3:np.matrix([[1, 2.5], [1+.5j, np.nan]])
 },
 {1, 3.4, 1+2j, np.nan, True, False, None, int, 'aa', os, sys, pd.concat}]
```

It should be noted that serialization of lambda is supported at code level, but functions are only serialized at surface name level. Therefore, in order to successfully deserialize functions, they have to be imported or defined first; and similarly for modules, they have to be imported in the first place. Otherwise, the resulting objects will be in the specially-coded string form which is nevertheless readable.