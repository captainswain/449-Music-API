import sqlite3
import uuid
import pugsql
from psycopg2.extensions import register_adapter,  AsIs


# register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
register_adapter(uuid.UUID, lambda u: u.bytes_le)


# # def addapt_numpy_float64(numpy_float64):
# #   return AsIs(numpy_float64)


# register_adapter(numpy.float64, addapt_numpy_float64)


queries = pugsql.module( os.path.abspath(os.path.dirname(__file__)) + '/queries/')

# queries.connect("sqlite:///main.db")

# conn = sqlite3.connect('test.db', detect_types=sqlite3.PARSE_DECLTYPES)

# c = conn.cursor()
# c.execute('CREATE TABLE test (guid GUID PRIMARY KEY, name TEXT)')

data = (uuid.uuid4(), 'foo')
print ('Input Data:', data)
c.execute('INSERT INTO test VALUES (?,?)', data)

c.execute('SELECT * FROM test')
print ('Result Data:', c.fetchone())



