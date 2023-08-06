from . import pd
from pyathena.connection import Connection
def getCalendars(columns,conn=Connection):
    return pd.read_sql("select "+columns +" from calendars", conn)