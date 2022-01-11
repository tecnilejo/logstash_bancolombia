from bson.objectid import ObjectId
from pymongo import MongoClient
import sys
import time
import re
contrato_id = sys.argv[1]
ci = sys.argv[2]
HOST = "172.30.5.3"
PORT = 30017
USER = "mosaicoadm"
PASSWORD = "m0s4iC0*AdM-"
DB = "mosaicodb"
coleccion = "dispositivos"
esto = ObjectId(contrato_id)

# host variables for MongoDB
DOMAIN = HOST
PORT = PORT

# create an instance of MongoClient()
client = MongoClient(
    host=DOMAIN + ":" + str(PORT),
    serverSelectionTimeoutMS=3000,  # 3 second timeout
    username=USER,
    password=PASSWORD
)
mydb = client[DB]
mycol = mydb[coleccion]
time.sleep(0.2)
mydoc = mycol.find({'contrato': esto})
# ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|[A-Za-z0-9_\-\.]{1,})
if re.match("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", ci):
    criterio = "ip"
else:
    criterio = "nombre"

for x in mydoc:
    if str(ci) == str(x[criterio]):
        r = (x["ip"])

s = re.findall(r'[_0-9.A-Za-z-:/]{1,}', r)[0]
# s=re.findall(r"[0-9.]{1,}",r)[0]
print(s)
