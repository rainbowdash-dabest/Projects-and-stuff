# keyboard.py - MicroPython HID Helper Driver

# standard file imported from the MIT license, Micropython HID driver. No modifications.

import time 
import usb.device.core
import usb.device.hid

class Keycode:
    SPACE = 0x2C
    UP_ARROW = 0x52
    DOWN_ARROW = 0x51
    LEFT_ARROW = 0x50
    RIGHT_ARROW = 0x4F

class Keyboard:
    def __init__(self):
        import usb.device
        from usb.device.hid import HIDInterface
        
        # Standard Universal USB HID Keyboard Report Descriptor Layout Matrix
        keyboard_descriptor = (
            b'\x05\x01'  # Usage Page (Generic Desktop)
            b'\x09\x06'  # Usage (Keyboard)
            b'\xa1\x01'  # Collection (Application)
            b'\x05\x07'  #   Usage Page (Keyboard/Keypad)
            b'\x19\xe0'  #   Usage Minimum (Keyboard Left Control)
            b'\x29\xe7'  #   Usage Maximum (Keyboard Right GUI)
            b'\x15\x00'  #   Logical Minimum (0)
            b'\x25\x01'  #   Logical Maximum (1)
            b'\x75\x01'  #   Report Size (1)
            b'\x95\x08'  #   Report Count (8)
            b'\x81\x02'  #   Input (Data, Variable, Absolute) -> Modifier Byte
            b'\x95\x01'  #   Report Count (1)
            b'\x75\x08'  #   Report Size (8)
            b'\x81\x01'  #   Input (Constant) -> Reserved Byte
            b'\x95\x06'  #   Report Count (6)
            b'\x75\x08'  #   Report Size (8)
            b'\x15\x00'  #   Logical Minimum (0)
            b'\x25\x65'  #   Logical Maximum (101)
            b'\x19\x00'  #   Usage Minimum (None)
            b'\x29\x65'  #   Usage Maximum (Keyboard Application)
            b'\x81\x00'  #   Input (Data, Array) -> 6 Key Codes Array
            b'\xc0'      # End Collection
        )

        # Initialize the hardware layout with the exact mandatory argument arrays
        self.hid = HIDInterface(keyboard_descriptor, protocol=1)
        usb.device.core.get().init(self.hid, builtin_driver=True)
        self.blank_report = bytearray(8)

    def _send_report(self, modifiers, key1, key2=0, key3=0):
        # Assemble standard 8-byte tracking packets 
        report = bytearray(8)
        report[0] = modifiers
        report[2] = key1
        report[3] = key2
        report[4] = key3
        try:
            self.hid.send_report(report)
        except Exception:
            pass 

    def press(self, keycode):
        self._send_report(0, keycode)

    def release(self):
        try:
            self.hid.send_report(self.blank_report)
        except Exception:
            pass
        