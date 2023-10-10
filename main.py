'''
Código principal
requiere la bibliotea PMSA_read

autor: Miguel Robles
'''

from machine import Pin, I2C, RTC
from time import sleep, time
from pmsa003 import PMSA_read
import datalog_lib as dlog
from info import *
import usocket as socket
import ssl
import network

#convierte de tupla de datos de fecha a cadena
#recibe la tupla y la zona horaria
def format_date(date, utc=0):
    #extrae info de tupla
    date = date[0:3] + date[4:7]
    #convierte UTC
    utc = '{:+03d}'.format(utc)
    #convirtiendo a cadena con formato
    date_str = [str(date[0])] +\
            ["{:02d}".format(e) for e in date[1:]]
    #uniendo 
    date_str = '-'.join(date_str[0:3]) + \
            'T'+':'.join(date_str[3:]) + utc
    return (date_str)

#realiza configuraciones iniciales
#regresa una lista con los objetos inicializados
def config():
    #configuración I2C
    i2c = I2C(0, scl=Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP),
              sda=Pin(21, Pin.OPEN_DRAIN, Pin.PULL_UP), freq=100000)
    print('i2c:', i2c.scan() )
    rtc = RTC()
    return i2c, rtc

def update_RTC(rtc):
    wlan = dlog.wlan_connect(ssid, password)
    if wlan == None:
        return None
    print(wlan.ifconfig())
    dlog.get_date_NTP(['1.mx.pool.ntp.org', 'cronos.cenam.mx'])
    wlan.active(False)
    return True


def mide(i2c):

    #lectura de datos PMSA
    data = PMSA_read(i2c)

    #definición de datos a obtener
    #PM1, PM2.5, PM10
    list_data= [
        'PM1.0_ugm3',
        'PM2.5_ugm3',
        'PM10_ugm3',
        #'1.0um_0.1L',
        #'2.5um_0.1L',
        #'10um_0.1L',
        ]
    #extrayendo sólo datos de interés
    #y convirtiendo a cadena
    data_str = [ str(data[name]) for name in list_data ]
    data_str = ','.join(data_str)

    return data_str

def save(data):
    pass

def send(data, wlan):
    timeout_send = 4.0
    #url de API
    url_server= "https://ruoa.unam.mx:8041/pm_api"
    #separa url, asume que incluye puerto y protocolo
    protoc, _, host = url_server.split('/',2)
    print(protoc, host)
    host, port = host.split(':')
    print('host:',host, port)
    wlan = dlog.wlan_connect(ssid, password)
    addr2 = socket.getaddrinfo(host, port)[0][-1]
    #addr2 = ('132.248.8.29', 8041)
    print('addr:', addr2)

    if wlan.isconnected() == False:
        wlan = dlog.wlan_connect(ssid, password)
    if wlan != None:
        print('conectado a', ssid)
        print('Enviando datos instantaneos a', host, data)
        #sock_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_send = socket.socket()
        test = socket.getaddrinfo("www.google.com", 443)[0][-1]
        print("test:", test)
        sock_send.settimeout(timeout_send)
        #sock_send.connect(test)
        #sock_send = ssl.wrap_socket(sock_send)
        #sock_send.write(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        #response = sock_send.read(200)
        #print('he:', response)
        #sock_send.close()
        try:
            sock_send.connect(addr2)
            print('connect')
            sock_send = ssl.wrap_socket(sock_send)
            sock_send.write(bytes('PUT /pm_api HTTP/1.1\r\n', 'utf8'))
            sock_send.write(bytes('Content-Length: %s\r\n' % (len(data)), 'utf8'))
            sock_send.write(bytes('Content-Type: text/csv\r\n\r\n', 'utf8'))
            sock_send.write(bytes(data, 'utf8'))
            print('send:', data)
            #sock_send.send(bytes('\r\n', 'utf8'))
            line =b''
            response=b''
            while line != b'0\r\n':
                line = sock_send.readline()
                print('line:', line)
                response+=line
            #response = sock_send.read(165)
            sock_send.close()
            if response!=b'':
                if response.split()[1] == b'201':
                    print('datos instantáneos recibidos')
            print('response:', response)
        except OSError:
            print ('No hay conexión con el servidor ', host)
    else:
        print('No se pido conectar a WiFi')
    wlan.active(False)

#definición de zona horaria
utc= -6
# definición de intervalos en [segundos]

# intervalo de medición y  almacenamiento
Δs = 60

# intervalo de verificación
Δt = Δs//5

# intervalo de actualización de RTC
ΔRTC = 60*60*1

i2c, rtc = config()

wlan = network.WLAN(network.STA_IF)
#send('test', wlan)

#banderas
flags={}
#actualización de RTC
flags['RTC'] = False
#envio de datos a servidor
flags['send'] = False

# tiempo actual (hora y fecha)
time_now = time()
# tiempo de siguiente medición
time_mide = time_now 

#tiempo de siguiente update RTC
time_RTC = time_now

while True:
    time_delta = time_now
    time_now = time()
    time_delta = time_now - time_delta

    #if time_RTC <= time_now:
        #if (update_RTC(rtc) == None):
            #print('update RTC fail!')
        #else:
            #time_RTC += ΔRTC
            #print('RTC update:', time_now)

    if time_mide <= time_now:
        time_mide += Δs
        #lectura de fecha
        date = rtc.datetime()
        #conversión de fecha
        date_str = format_date(date, utc=-6)
        data_str = date_str +','+ mide(i2c)
        print(data_str)
        save(data_str)
        send(data_str, wlan)

    if flags['send'] == True:
        send(data)
    sleep(Δt)
