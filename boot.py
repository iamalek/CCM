
#

try:
  import usocket as socket
except:
  import socket


from machine import Pin, I2C

import network
import ssd1106
import time
import dht


import esp
esp.osdebug(None)

import gc
gc.collect()


led = Pin(33, Pin.OUT)
led.value(0)
led_wifi_ok = Pin(2, Pin.OUT)
led_wifi_ok.value(0)
bip = Pin(19, Pin.OUT)
bip.value(0)

sensor = dht.DHT11(Pin(4))
display = ssd1106.SSD1106(pin_scl=Pin(22), pin_sda=Pin(21), height=64, external_vcc=False)

#display.invert_display(1)
x = 0
y = 0
direction_x = True
direction_y = True



display.fill(0)
display.text('CCM v1.0', 30, 20)
display.text('16.04.21', 30, 40)
#display.hline(0, 10, 127, 0xffff)
display.display()
time.sleep_ms(1000)

#pinsetup = Pin(2, Pin.IN, Pin.PULL_UP)
pinsetup = Pin(5, Pin.IN)
print("PinSetup = ", pinsetup.value())
if pinsetup.value() == 0:
  print("Pressed PinSetup")


display.fill(0)
display.text('Connect to wifi.', 0, 30)
display.display()

ssid = 'MGTS-GPON-6406'
password = 'VU9W7DAJ'
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

ip_addr = station.ifconfig()[0]

import uftpd_



display.fill(0)
display.text('FTP started on', 0, 20)
display.text(ip_addr, 0, 40)
display.display()
time.sleep_ms(2000)


bip.value(1)
time.sleep_ms(10)
bip.value(0)

led = Pin(33, Pin.OUT)
led_wifi_ok = Pin(2, Pin.OUT)
led_wifi_ok.value(1)
time.sleep_ms(100)
led_wifi_ok.value(0)
time.sleep_ms(100)
led_wifi_ok.value(1)
time.sleep_ms(100)
led_wifi_ok.value(0)
time.sleep_ms(100)
led_wifi_ok.value(1)
time.sleep_ms(100)
led_wifi_ok.value(0)
time.sleep_ms(100)
led_wifi_ok.value(1)

#out1 = Pin(33, Pin.OUT)

def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(1000)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

#data = http_get('http://micropython.org/ks/test.html')
#print(data)


# ############################
# Загрузка файла с веб сервера
#import usocket as socket
#addr = socket.getaddrinfo('raw.githubusercontent.com', 80)[0][-1]
#s = socket.socket()
#s.connect(addr)
#s.send(b'GET / HTTPS/1.1\r\nHost: https://raw.githubusercontent.com/robert-hh/FTP-Server-for-ESP8266-ESP32-and-PYBD/master/uftpd.py\r\n\r\n')
#data = s.recv(1000)
#s.close()
# ############################


