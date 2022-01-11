import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
asunto = "ALERTA EN GESTION DE EVENTOS"
mensaje = sys.argv[1]


def notificar(asunto, toaddr, mensaje):
    fromaddr = "monitoreomosaico@arus.com.co"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = asunto

    body = mensaje
    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()
    s.login(fromaddr, "Mayo4321*")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


notificar(asunto, "henry.calderon@arus.com.co", mensaje)
