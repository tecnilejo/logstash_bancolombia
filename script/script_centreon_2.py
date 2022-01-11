import subprocess
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


def OBTENER_IP(ci, id_con):
    import subprocess
    import re
    p1 = subprocess.Popen("/usr/bin/python2.7 /usr/share/logstash/script/consultar_ci.py '" +
                          id_con+"' '"+ci+"'", stdout=subprocess.PIPE, shell=True)
    (ip, err) = p1.communicate()
    ip = ip.replace("\n", "")
    return ip


def consultar(ip, servicio, servicio2):
    comando = "/usr/bin/curl -XGET https://172.30.5.3:3000/accion-critica/BancolombiaServiceManagement/5fad857e9220f63e27d8ce1c/" + \
        ip+"/"+servicio+"/"+servicio2+" -k"
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


if True:
    print("aprobado")
    ci = sys.argv[1]
    servicio = sys.argv[2]
    if "Disco" in servicio:
        servicio2 = "CRITICAL"
        ip = OBTENER_IP(ci, "5fad857e9220f63e27d8ce1c")
        print("esta es la ip:", ip)
        consultar(ip, servicio, servicio2)
    elif "SQL@" in servicio:
        print("tipo sql")
        servicio = servicio.split("SQL@")[1]
        print(servicio)
        servicio2 = "DOWN"
        ip = OBTENER_IP(ci, "5fad857e9220f63e27d8ce1c")
        print("esta es la ip:", ip)
        consultar(ip, servicio, servicio2)
    elif "CPU" in servicio:
        servicio2 = "CRITICAL"
        ip = OBTENER_IP(ci, "5fad857e9220f63e27d8ce1c")
        print("esta es la ip:", ip)
        consultar(ip, servicio, servicio2)

    else:
        servicio = servicio.split("SQL@")[0]
        servicio2 = "DOWN"
        ip = OBTENER_IP(ci, "5fad857e9220f63e27d8ce1c")
        print("esta es la ip:", ip)
        consultar(ip, servicio, servicio2)

    mensaje = "----------------------\n"+fecha_actual+" "+horas+"\nCI: "+ci+"\nIP: " + \
        ip+"\nCONTRATO: Bancolombia Service Management\n----------------------\n\n"

    s = open("/tmp/general.txt", "a")
    mensaje = mensaje.replace("----------------------\n"+fecha_actual,
                              "----------------------\n"+servicio2+"\n"+fecha_actual)
    s.write("Bancolombia Service Management "+servicio+" "+mensaje)
    s.close()
else:
    print("no esta en el rango de tiempo permitido")
