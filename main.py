'''
Código principal
requiere la bibliotea PMSA_read

autor: Miguel Robles
'''

from machine import Pin, I2C, RTC
from time import sleep_ms
from pmsa003 import PMSA_read

#realiza configuraciones iniciales
#regresa una lista con los objetos inicializados
def config():
    #configuración I2C
    i2c = I2C(0, scl=Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP),
              sda=Pin(21, Pin.OPEN_DRAIN, Pin.PULL_UP), freq=100000)
    print(i2c.scan() )
    rtc = RTC()
    return i2c, rtc

def update_RTC(rtc):
    pass


def mide(i2c):
    #lectura de fecha
    date = rtc.datetime()

    #conversión de fecha
    date = date[0:3] + date[4:7]
    date_str = [str(date[0])] +\
            ["{:02d}".format(e) for e in date[1:]]
    #date_str = date_str.join(',')

    print('date', date_str, end=' ')

    #lectura de datos
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
    data2 = [ str(data[name]) for name in list_data ]
    print( 'data2', date_str +data2)

    for i,name in enumerate(list_data):
        print(data[name], end=' ')
    return data

def save(data):
    pass

def send(data):
    pass


#tiempo de muestreo en segundos
ts = 60
#conversión a milisegundos
ts *= 10**3


i2c, rtc = config()
while True:
    update_RTC(rtc)
    data = mide(i2c)
    save(data)
    send(data)
    sleep_ms(ts)
