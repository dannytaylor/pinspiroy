# pinspiroy

pinspiroy is a linux driver workaround for the [Huion Inspiroy G10T](https://www.huiontablet.com/g10t.html). Note that this is not a driver, it is a user land implementation that creates virtual devices with uinput to mimic the tablet functionality.

All features of the tablet are working with this, but it isn't an ideal fix. Also I'm not really familiar with python so this might be implemented poorly. Hopefully this could be helpful for someone smarter than me to make a proper driver.

## Requirements
- [pyusb](https://walac.github.io/pyusb/) (pip install pyusb)
- [python-evdev](https://github.com/gvalkov/python-evdev) (pip install evdev)
- some things that should be already installed (libusb1.0, uinput) 

## Usage
_$ sudo python pinspiroy.py_

You may need to first connect the device to a Windows VM to flip the tablet into full-functioning mode. This mode should persist on reboot and without the VM, but will not persist on reconnecting the USB dongle.

Configuration values are found in config.py. Currently it's just bools for rotating axes for left-handed use and disabling the trackpad. The pad buttons are setup to change positions when rotated also.

Button and gesture bindings are found in bindings.py. Note: If you're adding new keys to your bindings you will have to add them to the virtual button pad capabilities: see 'cap_btn' in pinspiroy.py

## Troubleshooting
This program requires the uinput module to be loaded. Either manually (_sudo modprobe uinput_)
or automatically on boot; [see the Arch wiki](https://wiki.archlinux.org/index.php/Kernel_modules).

**Insufficient permissions:** This program requires access to read USB data (pyusb/libusb) and create and write to the virtual devices(python-evdev/uinput). Either run as superuser or add the appropriate permissions where needed.

**Pen not moving on contact, buttons and trackpad working:** This seems to be a problem with libinput requiring a pen resolution; changing the resolution with python-evdev doesn't seem to work. Check that you don't have a libinput driver catchall rule for tablets in your xorg.conf.d/. You may need a evdev driver catchall rule for tablets.

**Key error: NUM:** Run the debug.py file to see the array data the tablet is sending. The first array value should be 8. If it isn't (probably will be 10) the tablet isn't in full tablet mode. See usage section.

Still working out some of the problems, but feel free to tweet @ me or open an issue.

## TODO:
- Figure out USB data to send to the tablet to flip it to full functioning mode so Windows VM not needed
- Add ability to be able to use tablet in not fully-functioning mode (with impaired resolution and no gesture support)
- Get stylus buttons working.
