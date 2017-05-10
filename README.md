## Pinspiroy

Pinspiroy is a driver workaround for the [Inspiroy Huion G10T](https://www.huiontablet.com/g10t.html). Note that this is not a driver, it is a user land implementation that creates a virtual device to mimic the tablet data.

All features of the tablet are working with this, but it isn't an ideal fix. Hopefully thi


### Requirements
- python3
- pyusb (pip install pyusb)
- python-evdev (pip install evdev)
- some things that should be already installed (libusb, uinput) 

### Usage
sudo python pinspiroy.py

Configuration values are found in config.py. Currently it's just rotating axes for left-handed use and disabling the trackpad.

Button and gesture binding are found in btn_id.py and gst_id.py. If you're adding new keys to your bindings you will have to 

## Troubleshooting
This program requires the uinput module to be loaded. Either manually (_sudo modprobe uinput_)
or automatically; [see the Arch wiki](https://wiki.archlinux.org/index.php/Kernel_modules)

**Insufficient permissions:** This program requires access to read usb data and create and write to the virtual devices. Either run as superuser or add the appropriate permissions where needed.

**Pen not moving on contact:** check that you don't have a libinput driver catchall rule for tablets in your xorg.conf.d/. I can't seem to set the resolution of the pen surface and libinput doesn't like that. You may need a evdev driver catchall rule for tablets.

