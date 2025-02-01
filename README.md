
# Goal

My Wife works as a Psych NP and meets with clients in her office. I have had the tendency of walking in and asking odd questions in weird accents. Everyone finds it funny but its very inappropriate so there had to be a way to alert everyone that she cant be disturbed. We got a nice little RGB lamp outside of her office that's key'd to a button through home assistant and it works perfectly. Only problem is she cant see what color it is so shell leave it on RED all day.

## Solution

I thought having a small cube of light on her desk that's the same as the lamp outside would be a perfect solution. I found nothing and anything that was even remotely close was very expensive and still very large. I figured it cant be that hard to make what i want. I got to jerry rigging and came up with an esp32 (what i had on hand) and a RGB led diode and a button. wrote a circuit python script that would use the exact same functions as the button in Home Assistant. 

# requirements 

- ESP32 Board
- Push Button connected to GPIO 0 (or any preferred GPIO)
    - I used the button attached to the other switch
- RGB LED connected to GPIOs 2, 3, and 4  (or any preferred GPIOs)
- [CircutPython Firmware Installed](https://learn.adafruit.com/circuitpython-with-esp32-quick-start/web-serial-esptool)

# GPIO pinout

- Single Press - Blue LED (D4)
- Long Press (800ms+) - Green LED (D3)
- Double Tap (within 500ms) - Red LED (D2)

<p align=center>
<img src=assets/pinout.png width=500>
</p>

After I breadboarded the controller and LED, i started to think about form factor. At fist i thought i would just use a button and have it wedged in-between the HA button and the ESP32, then i figured "the HA button as a button in it, why not just steal that signal". After soldering a line and checking polarity, i figured id go one step farther and also just steal the battery (at this point i wondered if i should actually just make the ESP32 board itself be the button for both as it could support Matter and Zigbee. project for another day), this......worked......but not really. 
` In this image, I wired the postive and negative incorrect`
<p align=center>
<img src=assets/CircutBoard.jpeg width=500>
</p>
the 3V the battery was outputting wasn't enough to support everything. the ESP32 would work but couldn't pass enough to actually light the LED like i wanted. 



So i attached the 3v, GND, and D0 to the board of the HA button. verified everything worked, stuck it back together and now i have a functional button that also shows the color of the lamp at her desk. Its not perfect but for spending about 2-3 hours between soldering, programming, and testing, id consider it a success! I will (maybe/hopefully) return to this to make a more professional version with a light diffuser and just have the entire object 
<p align=center>
<img src=assets/Button1.jpeg width=200>
  <img src=assets/Button2.jpeg width=200>
  <img src=assets/Button3.jpeg width=200>
</p>

<p align=center>
<img src=assets/Blue.jpeg width=200>
  <img src=assets/Red.jpeg width=200>
  <img src=assets/Green.jpeg width=200>
</p>

