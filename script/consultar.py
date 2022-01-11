import sys
contrato= sys.argv[1]
HOST = "172.30.5.3"
PORT = 30017
USER = "mosaicoadm"
PASSWORD = "m0s4iC0*AdM-"
DB = "mosaicodb"
coleccion = "contrato"
from pymongo import MongoClient
import re

# host variables for MongoDB
DOMAIN = HOST
PORT = PORT

# create an instance of MongoClient()
client = MongoClient(
    host = DOMAIN + ":" + str(PORT),
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username = USER,
    password = PASSWORD
)
mydb = client[DB]
mycol = mydb[coleccion]
mydoc = mycol.find({'contrato': contrato}, {'contrato': 1})

for x in mydoc:
  r=str(x)

s=re.findall(r"[0-9a-z]{1,}",r)[4]
print(s)

