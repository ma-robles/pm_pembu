'''
Biblioteca para lectura de sensor PMSA003I
requiere definición previa del puerto I2C

'''

from ustruct import unpack

def PMSA_read(i2c):
    data_len = 0x20
    dev_dir = 18
    data_names = [
        'st1',
        'st2',
        'ndata',
        'PM1.0_CF',
        'PM2.5_CF',
        'PM10_CF',
        'PM1.0_ugm3',
        'PM2.5_ugm3',
        'PM10_ugm3',
        '0.3um_0.1L',
        '0.5um_0.1L',
        '1.0um_0.1L',
        '2.5um_0.1L',
        '5um_0.1L',
        '10um_0.1L',
        'ver',
        'error',
        'chksum',
        ]
    data_val = i2c.readfrom(dev_dir, data_len)
    data_val = unpack('>BBHHHHHHHHHHHHHBBH', data_val)
    data={}
    for i,name in enumerate(data_names):
        data[name]=data_val[i]
    return data

