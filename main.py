import json
import pyodbc
from ExchangeRateAPI import getExchangeRates
from MSSQLAPI import *



exchangeRateJSON = getExchangeRates()
parsed = json.loads(exchangeRateJSON.content)
print(json.dumps(parsed, indent=4, sort_keys=True))


conn = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=tcp:109.121.61.9,1433;"
        #"Server=DESKTOP-1D3F65B\SQLEXPRESS;"
        "Database=CryptoMenjacnica;"
        "UID=Isidora Bogdanovic;"
        "PWD=drs123;"
    )

read(conn)
create(conn)
read(conn)
update(conn)
read(conn)
delete(conn)
read(conn)
conn.close()




