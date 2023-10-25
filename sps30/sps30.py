from machine import I2C
from ustruct import unpack

addr_sps30 = 0x69
#checksum calculation
#return 8 bytes
#data is 2 bytes array
#data = bytes([0xbe, 0xef])
def calc_crc(data):
    crc = 0xff
    for d in data:
        crc ^= d
        for i in range(8):
            if (crc & 0x80 != 0):
                crc = (crc << 1) ^ 0x31
            else:
                crc <<= 1
    return crc & 0xff
#test
#print(hex(calc_crc(bytes([0xbe, 0xef]))))

def set_read(i2c, pointer, nbytes):
    #pointer type = array of bytes
    i2c.writeto(addr_sps30, pointer)
    return i2c.readfrom(addr_sps30, nbytes)

def set_write(i2c, pointer, data):
    #pointer and data tyep =  array of bytes
    return i2c.writeto(addr_sps30, pointer+data)

def read_meas(i2c):
    dnames = [
        "PM1.0_ugm3",
        "PM2.5_ugm3",
        "PM4.0_ugm3",
        "PM10_ugm3",
        "PM0.5_ncm3",
        "PM1.0_ncm3",
        "PM2.5_ncm3",
        "PM4.0_ncm3",
        "PM10_ncm3",
        "size_um",
        ]

    data_val = unpack('>HBHBHBHBHBHBHBHBHBHB', 
                      set_read(i2c, bytes([0x03,0]), 30) )
    data = {}
    for i,n in enumerate(dnames):
        data[n] = data_val[i*2]
    return data

def read_ver(i2c):
    return set_read(i2c, bytes([0xd1,0]), 3)

def start(i2c):
    #data type = integer
    dtype = 0x05
    buf = bytes([dtype, 0x00, calc_crc(bytes([dtype,0]))])
    set_write(i2c, bytes([0,0x10]), buf)
    return None

#i2c = I2C(0, scl=Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP),
#    sda=Pin(21, Pin.OPEN_DRAIN, Pin.PULL_UP), freq=100000)
#
#start(i2c)
#sleep(3)
#
#while True:
#    data = read_meas(i2c)
#    print(data)
#    sleep(1)
