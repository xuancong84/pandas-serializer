# pandas-serializer
A utility for convenient save/load of Python objects containing pandas DataFrame/Series, can be nested containers.
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

The working principle is first convert every non-convertible object (such as DataFrame/Series/types/modules) into a specially-coded string, then use Python repr() to convert the entire object in one go.
In addition, this powerful utility will also try to convert/restore other non-reverse-convertible Python objects such as types, modules, functions, etc. However, there is no guarantee so those data types should be avoided in general.
