# sleep-debugger

This project aims to create an open source, non-invasive sleep debugger. There are a lot of sleep monitoring tools out there,
but often they require you to wear wrist-bands, head gear or other stupid things. Even then most don't work well and in all
the cases I've seen, they are closed and you do not get to manage your own data.

The goals of this project include:

- Use open source software to build a sleep monitoring system that is actually useful.
- Build a non-invasive system. This means that it should not alter your sleeping environment in order to gather data. No electrodes 
  on your body, lights or other things that could influence your sleep. Afterall, sleep is supposed to get better with this device!
- Put the data collected into your hands, not some corporation that is going to sell your data.


# Supported sensors

Most of these sensors are ones I already had at home, so I used them. I really recommend the HTU21D-F temperature/humitidy
sensor since it is very good, albeit expensive. The accelerometers and light sensors matter less, but I recommend digital
i2c interfaces for whichever break out boards you choose.

* Triple-axis Accelerometer+Magnetometer 

  buy: https://www.adafruit.com/product/1120 
  lib: https://github.com/adafruit/Adafruit_Python_LSM303

* Adafruit HTU21D-F Temperature & Humidity Sensor Breakout Board 

  buy: https://www.adafruit.com/product/1899 
  lib: 
  needs: https://github.com/bbx10/htu21dflib.git

* VCNL4010 Proximity/Light sensor 
  
  buy: https://www.adafruit.com/product/466
  notes: I didn't like this one -- between I2C bus problems and fragility of the sensors, I've stopped using this one. See the TMT6000 

* TMT6000 via attiny "ADC"


# Target audience

Current target audience: Geeks who love Raspberry Pis and have tools to solder wires to sensors to build their own
setup. If you do not really fit this description, then please wait until this project reaches some more maturity and
becomes more accessible for non-geeks.


# How to help

If you're interested in helping, get a Raspberry Pi (any should work, but a 3 or Zero W are best) an accelerometer,
temperature/humidity and light sensor. Wire them to your Raspberry Pi. Place the accelerometer onto your bed (I 3D printed
a light plastic case for mine) so it can measure your movements as you sleep.

Next steps include:

- Writing data analysis to figure out when a user starts/stops sleeping.
- Write a morning sleep report that gives the user an idea of how they slept the night before.
- Create a more friendly sleep graphing system than Grafana. Grafana is really nice, but suited for geeks -- we'd need to do
better.


# Caveats

I doubt this setup will collect good data if you sleep with a partner. Currently the setup is geared towards one 
person sleeping by themselves. If you're having trouble sleeping with a partner in bed, your first step should be to sleep by
yourself!
