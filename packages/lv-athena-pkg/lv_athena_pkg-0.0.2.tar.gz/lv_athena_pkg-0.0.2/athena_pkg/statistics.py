from . import pd
from pyathena.connection import Connection
def numberOfAvailableNights(date='YYYY-MM-DD',conn=Connection):
    """ Get Number of nights available by year,month or day"""
    return pd.read_sql("select count(*) from calendars where date like'"+date+"'",conn)['_col0'][0]