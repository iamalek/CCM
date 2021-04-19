print("This main.py")

# Make sure the corners are active
#display.set_pixel(0,   0,  1)
#display.set_pixel(0,   3,  1)
#display.set_pixel(3,   0,  1)
#display.set_pixel(3,   3,  1)
#display.set_pixel(127, 0,  1)
#display.set_pixel(0,   63, 1)
#display.set_pixel(127, 63, 1)

display.fill(0)
display.text('TEMP', 0, 10)
display.text('HUMD', 0, 30)
display.display()

#sensor.measure()
temp = sensor.temperature()
humd = sensor.humidity()
print("TEMP ", temp)
print("HUMD", humd)

display.fill_rect(40-3, 10-3, ((8*4)+3)+3, (8+3)+2, 1)
display.text(str(temp), 40, 10, 0)
display.fill_rect(40-3, 30-3, ((8*3)+3)+3, (8+3)+2, 1)
display.text(str(humd), 40, 30, 0)
display.display()

display.text('(65.0)', 80, 10)
display.text('(80%)', 80, 30)
display.display()

display.hline(0, 50, 127, 1)

display.rect(10-2, 55-2, ((8*1)+2)+2, (8+3), 1)
display.text('1', 10, 55)
display.fill_rect(28, 53, 12, 12, 1)
display.text('2', 30, 55, 0)
display.rect(50-2, 55-2, ((8*1)+2)+2, (8+3), 1)
display.text('3', 50, 55)
display.rect(70-2, 55-2, ((8*1)+2)+2, (8+3), 1)
display.text('4', 70, 55)
display.rect(90-2, 55-2, ((8*1)+2)+2, (8+3), 1)
display.text('5', 90, 55)
display.rect(110-2, 55-2, ((8*1)+2)+2, (8+3), 1)
display.text('6', 110, 55)
display.display()

try:
    import urequests as requests
except ImportError:
    import requests

#r = requests.get("https://raw.githubusercontent.com/robert-hh/FTP-Server-for-ESP8266-ESP32-and-PYBD/master/uftpd.py")
#print(r)
#print(r.content)
#print(r.text)
#print(r.json())

# It's mandatory to close response objects as soon as you finished
# working with them. On MicroPython platforms without full-fledged
# OS, not doing so may lead to resource leaks and malfunction.

#file = open ("uftpd_.py", "w")
#print(type(file))
#file.write(r.text)
#r.close()
#file.close()

#import os
#os.listdir()
#file = open ("uftpd_.py", "r")
#print(file.read())
#file.close()

