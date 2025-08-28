from machine import SDCard
import os
import ntptime
import network
from time import sleep

def check_SD(sd, path = '/sd' ):
    #sd = SDCard( slot =2, freq =1000000)
    #print(sd) 
    try:
        os.mount(sd ,path )
        #os.umount( path)
    except:
        return False
    return True

def get_date_NTP( host_list = ["cronos.cenam.mx"]):
    # sincroniza hora con servidor NTP
    # devuelve False si no se logra
    for host in host_list:
        print('NTP:', host, '...', end=' ')
        ntptime.host = host
        try:
            ntptime.settime()
            print('conectado')
            return True
        except:
            print('no conectado!')
    return False

def wlan_connect(ssid ,password):
    ''' activa y conecta la red WiFi '''
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active( True )
        #print(wlan.scan())
        wlan.connect(ssid ,password)
        n= 0
        print("Conectando a", ssid, end =' ')
        while not wlan.isconnected():
            print('*', end= '')
            sleep(1)
            n+= 1
            if n>10:
                break
    except:
        pass
    if not wlan.isconnected():
        wlan.disconnect()
        wlan.active( False)
        return None
    return wlan
