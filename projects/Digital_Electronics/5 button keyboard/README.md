## Macrokeyboard for iPad [Pi Pico H] (USB-C compatible)

Made this project because I needed to repeatedly pause a Blender tutorial on youtube on my ipad, and getting a whole keyboard when I just needed 5 buttons felt like too much.

<p align="center">
  <span style="display: inline-block; width: 70%; vertical-align: top; text-align: center;">
    <img src="../photos/HID_circuit.jpeg" width="100%" />
    <small> Breadboard Circuit </small>
  </span>
</p>

.execution-heirarchy__ to reboot, ground pin_0 to enter safe_mode. If key press registered, LED will flash.\
You can modify hold_down repeat rate to spam faster / autoclick.
Compatible with most USB-C devices.

.specifications and libs__ HID's are often bluetooth or wifi compatible, so the libs are downloaded externally when needed. My pico H did not have that convenience, so I with some trial and error, I integrated the usb - hid.py and core.py, and structured them without much modification. the only other file here is the keyboard.py HID driver, which is again a downloaded standard file from the micropython lib.
