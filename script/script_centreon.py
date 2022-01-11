import sys
import os
import time
import datetime
from datetime import datetime
import pytz
a = pytz.timezone("America/Bogota")
now = datetime.now(a)
horas = now.strftime("%H:%M")
fecha_actual = now.strftime("%d-%m-%Y")
horas2 = True


def OBTENER_IP(ci, id_con):
    import subprocess
    import re
    p1 = subprocess.Popen("/usr/bin/python2.7 /usr/share/logstash/script/consultar_ci.py '" +
                          id_con+"' '"+ci+"'", stdout=subprocess.PIPE, shell=True)
    (ip, err) = p1.communicate()
    ip = ip.replace("\n", "")
    return ip


def consultar(contrato, id, ip, servicio, servicio2):
    comando = "/usr/bin/curl -XGET https://172.30.5.3:3000/accion-critica/" + \
        contrato.split(' ')[0].capitalize()+"/"+id.replace('\n',
                                                           '')+"/"+ip+"/"+servicio+"/"+servicio2+" -k"
    print("este es el comando con que activa el agente: ", comando)
    p = subprocess.Popen(comando, stdout=subprocess.PIPE, shell=True)
    (res, err) = p.communicate()
    print("esta es la respuesta de la ejecucion del comando: ", res)
    if "ERROR" in res or '' == res or '{"code":404}' == res or "502 Bad Gateway" in res:
        print("notificara el error")
        mensaje = "'el comando que llama al agente es: "+str(comando)+"'"
        p = subprocess.Popen("/usr/bin/python2.7 /usr/share/logstash/script/notifica.py " +
                             mensaje, stdout=subprocess.PIPE, shell=True)
        (salida, err) = p.communicate()
    else:
        print("------El resultado de la operacion es OK------")


if horas2:
    print("aprobado")
    ci = sys.argv[2]
    ip = sys.argv[3]
    contrato = "BANCOLOMBIA MTAAS."
    servicio = sys.argv[1]
    if servicio == "DOWN":
        servicio = "Disponibilidad"
    if servicio == "uptime":
        servicio = "Uptime"
    if "Disco" in servicio or servicio == "CPU" or servicio == "Memoria" or servicio == "Uptime" or "3PAR_" in servicio:
        servicio2 = "CRITICAL"
    else:
        servicio2 = "DOWN"

    import subprocess
    p = subprocess.Popen("/usr/bin/python2.7 /usr/share/logstash/script/consultar.py '" +
                         contrato+"'", stdout=subprocess.PIPE, shell=True)
    (id, err) = p.communicate()
    id = id.replace("\n", "")

    print("este es el id del contrato: ", id)
    ip = OBTENER_IP(ci, id)
    print("esta es la ip:", ip)
    consultar(contrato, id, ip, servicio, servicio2)

    mensaje = "----------------------\n"+fecha_actual+" "+horas+"\nCI: " + \
        ci+"\nIP: "+ip+"\nCONTRATO: "+contrato+"\n----------------------\n\n"

    s = open("/tmp/general.txt", "a")
    mensaje = mensaje.replace("----------------------\n"+fecha_actual,
                              "----------------------\n"+servicio2+"\n"+fecha_actual)
    s.write(contrato+" "+servicio+" "+mensaje)
    s.close()
else:
    print("no esta en el rango de tiempo permitido")
