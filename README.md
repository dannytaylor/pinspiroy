## Pinspiroy

Pinspiroy is a driver workaround for the [Inspiroy Huion G10T](https://www.huiontablet.com/g10t.html). Note that this is not a driver, it is a user land implementation that creates a virtual devices with uinput to mimic the tablet data.

All features of the tablet are working with this, but it isn't an ideal fix. Also I'm not really familiar with python so this might be implemented poorly. Hopefully this could be helpful for someone smarter than me to make a proper driver.


### Requirements
- pyusb (pip install pyusb)
- python-evdev (pip install evdev)
- some things that should be already installed (libusb, uinput) 

### Usage
_$ sudo python pinspiroy.py_

Configuration values are found in config.py. Currently it's just bools for rotating axes for left-handed use and disabling the trackpad. The pad buttons are setup to change positions when rotated also.

Button and gesture binding are found in btn\_id.py and gst\_id.py. Note: If you're adding new keys to your bindings you will have to add them to the button pad capabilities: see 'cap_btn'  in pinspiroy.py

## Troubleshooting
This program requires the uinput module to be loaded. Either manually (_sudo modprobe uinput_)
or automatically on boot; [see the Arch wiki](https://wiki.archlinux.org/index.php/Kernel_modules).

**Insufficient permissions:** This program requires access to read USB data (pyusb/libusb) and create and write to the virtual devices(python-evdev/uinput). Either run as superuser or add the appropriate permissions where needed.

**Pen not moving on contact:** This seems to be a problem with libinput requiring a pen resolution; changing the resolution with python-evdev doesn't seem to work. Check that you don't have a libinput driver catchall rule for tablets in your xorg.conf.d/. You may need a evdev driver catchall rule for tablets.

**Key error: ##:** Run the read.py file to see the array data the tablet is sending. The first array value should be 8. If it isn't (probably will be 10) the tablet isn't in full tablet mode. I'm still figuring out how to flip it into the correct mode consistently. If you've used another Huion tablet on the computer since last using the G10T this will probably happen. Connecting then disconnecting the G10T in Windows with the manufacturer driver installed should correct this problem for now. This can be done in a VM or natively.
