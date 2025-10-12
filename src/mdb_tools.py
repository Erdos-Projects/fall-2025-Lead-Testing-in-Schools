import subprocess
import pandas as pd
import numpy as np
import simple_ddl_parser as ddl

# This module requires `mdbtools` to be installed in your $PATH

# This class wraps the other functions in this module and is recommended.
# Instantiate with `Mdb('file.mdb')`.
class Mdb:
    def __init__(self, mdb_file, encoding='utf8'):
        self.mdb_file = mdb_file
        self.encoding = encoding

    def mdb_schema(self):
        return _mdb_schema(self.mdb_file, self.encoding)

    def panda_schema(self):
        return _panda_schema(self.mdb_schema())

    def list_tables(self):
        return list(self.mdb_schema().keys())

    def panda_table(self, table_name, *args, **kwargs):
        ps = self.panda_schema()
        dtypes = ps[table_name]
        if dtypes != {}:
            kwargs['dtype'] = dtypes
        proc = subprocess.Popen(['mdb-export', self.mdb_file, table_name], stdout=subprocess.PIPE)
        return pd.read_csv(proc.stdout, *args, **kwargs)

    def panda_tables(self, *args, **kwargs):
        pandas = {}
        for n in self.list_tables():
            # It seems like sometimes list_tables() returns a name that doesn't exit in the actual database...
            # I think this is a whitespace issue, but haven't tried to debug enough.
            # However, the tables affected by this seem less important, and so we'll just skip on an error.
            try:
                pandas[n] = self.panda_table(n, *args, **kwargs)
            except:
                print("Error processing table " + n)
        return pandas





def __strip_quotes(obj):
    match obj:
        case str():
            return obj.removeprefix('"').removesuffix('"')
        case dict():
            return {__strip_quotes(k): __strip_quotes(v) for k,v in obj.items()}
        case list():
            return [__strip_quotes(v) for v in obj]
        case _:
            return obj

    # if isinstance(obj, str):
    #     return obj.removeprefix('"').removesuffix('"')
    # elif isinstance(obj, dict):
    #     return {__strip_quotes(k): __strip_quotes(v) for k,v in obj.items()}
    # elif isinstance(obj, list):
    #     return [__strip_quotes(v) for v in obj]
    # else:
    #     return obj

def __clean_columns(columns):
    def __popper(c, n):
        v = c.pop(n)
        return (v, c)
    return dict(__popper(c, 'name') for c in columns)

def _mdb_schema(mdb_file, encoding='utf8'):
    sql_schema = subprocess.check_output(['mdb-schema', mdb_file]).decode(encoding)
    # DDLParser doesn't quite like the fact that names are surrounded in [], so we change these to quotes before parsing.
    sql_schema = sql_schema.replace('[', '"').replace(']', '"')
    parsed = ddl.DDLParser(sql_schema).run(group_by_type=True)['tables']

    return __strip_quotes({t['table_name']: __clean_columns(t['columns']) for t in parsed})


def _panda_schema(mdbSchema):
    def __to_numpy_type(t):
        tp = t.get('type', 'Unknown').lower()
        if tp.startswith('double'):
            return np.float_
        elif tp.startswith('long') or (tp.startswith('numeric') and t['size'][1] == 0):
            return np.int_
        elif tp.startswith('text'):
            return np.str_
        else:
            return np.str_
    return {k: __to_numpy_type(v) for k,v in mdbSchema.items()}

# This is an option if you don't want to explicitly use the MDB class
def read_table(mdb_file, table_name, *args, **kwargs):
    encoding = kwargs.pop('encoding', 'utf8')
    mdb = MDB(mdb_file, encoding)
    return mdb.panda_table(table_name, *args, **kwargs)

# This is an option if you don't want to explicitly use the MDB class
def read_tables(mdb_file, *args, **kwargs):
    encoding = kwargs.pop('encoding', 'utf8')
    mdb = MDB(mdb_file, encoding)
    return mdb.panda_tables(*args, **kwargs)
