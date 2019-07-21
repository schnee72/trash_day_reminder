# trash day reminder
This a python script that runs on a Raspberry Pi and notifies me when it is time to take out the trash and the recycling. If it is trash day it lights up on LED, if it is also the day to take out the recycling, it will light a different LED. So I never have to guess. It figures out if it is a holiday week, what the proper day is. It also displays the time on a 7 segment LED and the temperature on another 7 segment LED.

It uses a DHT22 sensor for the temperature. It utilizes the Adafruit DHT library as well as the Adafruit LED Backpack library for the 7 segment LEDs. 

I put the stuff.py script in the /home/pi directory and made it executable with the following command:
```
chmod +x /home/pi/stuff.py
```
I added stuff.service file to /etc/systemd/system/multi-user.target.wants so that systemd will autostart the script. The contents of stuff.service is:
```
[Unit]
Description=Stuff
After=muti-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/stuff.py
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
Works like a charm.
