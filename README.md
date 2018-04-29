### Pen tablet functionality seems to be broken after a system update on Archlinux. Driver still works on Ubuntu 16.04, but not subsequent versions. Seems to be an issue with the newer Linux kernel and how uinput interprets BTN\_TOOL\_PEN.

# pinspiroy

pinspiroy is a linux driver workaround for the [Huion Inspiroy G10T](https://www.huiontablet.com/g10t.html). Note that this is not kernel-level driver, it is a user land implementation that creates virtual devices with uinput to mimic the tablet functionality.

All features of the tablet (except stylus side buttons) are working with this, but it isn't an ideal fix. Also I'm not too familiar with python so this might be implemented poorly. Hopefully this could be helpful for someone smarter than me to make a proper driver. If it this is helpful (or not working) for you I'd love to know! [@xhiggy](https://twitter.com/xhiggy)

## Requirements
- [pyusb](https://walac.github.io/pyusb/) (pip install pyusb)
- [python-evdev](https://github.com/gvalkov/python-evdev) (pip install evdev)
- pygtk for screen size detection (pip install pygtk)
- some things that should be already installed (libusb1.0, uinput) 

## Usage
_$ sudo python pinspiroy.py [usersettings.py]_

If no settings file is given it will load the *default.py* file. Custom settings files must be in the repo folder with a .py extension.


## Configuration
Custom configuration can be done via the *pinwiz.py* tool provided. It will export a configuration file to the working folder which can be passed to the pinspiroy script when run. The pinwiz tool very simple with no error checking for invalid settings, so be careful with your inputs and debug the exported file with a text editor if needed.

Default configuration values are found in default.py. It has settings for rotating axes for left-handed use and disabling the trackpad (I find it gets in the way). The pad buttons and gestures are setup to change bindings when rotated also.

Simple pressure curves and thresholds can be set, however I'd recommend using your art programs pressure adjustments instead of these options.

The default bindings set up with the following for defaults. These are set up to work best with Krita, so you may need to change them depending on your art program.

![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/buttons.png)

Buttons clockwise from top left of trackpad:
```
button1: left control (hold)	# eyedropper
button2: E			# eraser tool
button3: spacebar (hold)	# pan tool
button4: shift (hold)		# brush resizer
button5: ctrl + shift + z	# redo
button6: ctrl + z		# undo
```

Trackpad gestures:
```
Two fingers:
up/down/left/right: arrow keys

Three fingers:
up/down:            ctrl + +/-  # zoom in/out 		
left/right:         ctrl + [/]  # rotate cc/c

Taps:
one finger:         mouse left
two fingers:        mouse right
three fingers:      mouse middle

Pinch in/out:       unbound

```

For multimonitor setups you will need to enter the **screen** offset from the top left to the top left corner of the target **display** as well as the dimensions of the target display. For single monitor setups the offsets are both zero. My monitor setup is shown below as an example

![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/monitors.png)

## Troubleshooting
This program requires the uinput module to be loaded. Either manually (_sudo modprobe uinput_)
or automatically on boot; [see the Arch wiki](https://wiki.archlinux.org/index.php/Kernel_modules).

**Insufficient permissions:** This program requires root access to read USB data (pyusb/libusb). You could add this to your sudoers file to run at start without password entry, but that is not recommended for security reasons.

**Pen not moving on contact, buttons and trackpad working:** This seems to be a problem with libinput requiring a pen resolution; changing the resolution with python-evdev doesn't seem to work. Check that you don't have a libinput driver catchall rule for tablets in your xorg.conf.d/. You may need a evdev driver catchall rule for tablets.

**Key error: NUM:** Run the debug.py file to see the array data the tablet is sending. The first array value should be 8. If it isn't (probably will be 10) the tablet isn't in full tablet mode. See usage section.

Still working out some of the problems, but feel free to tweet @ me or open an issue.

## Thanks and Additional Reading
- Thanks to [@KaiJan57](https://github.com/KaiJan57) for the magic code to get around the Windows VM requirement
- Thanks to [@DevinPentecost](https://github.com/DevinPentecost) for general python help
- [event codes for uinput use can be found here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h)
- [more event code information found here](https://www.kernel.org/doc/Documentation/input/event-codes.txt)
- [useful tutorial for writing a USB driver with PyUSB](https://www.linuxvoice.com/drive-it-yourself-usb-car-6/)


![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/spin2.gif)
