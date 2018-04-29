### Pen tablet functionality seems to be broken after a system update on Archlinux. Driver still works on Ubuntu 16.04. Seems to be an issue with the newer Linux kernel and how uinput interprets BTN\_TOOL\_PEN. Downgrading the kernel doesn't seem to fix the issue, may have to recompile the uinput module from an older kernel (<4.11) manually.

# pinspiroy

pinspiroy is a linux driver workaround for the [Huion Inspiroy G10T](https://www.huiontablet.com/g10t.html). Note that this is not kernel-level driver, it is a user land implementation that creates virtual devices with uinput to mimic the tablet functionality.

All features of the tablet (except stylus side buttons) are working with this, but it isn't an ideal fix. Also I'm not too familiar with python so this might be implemented poorly. Hopefully this could be helpful for someone smarter than me to make a proper driver. If it this is helpful (or not working) for you I'd love to know! [@xhiggy](https://twitter.com/xhiggy)

## Requirements
- [pyusb](https://walac.github.io/pyusb/) (pip install pyusb)
- [python-evdev](https://github.com/gvalkov/python-evdev) (pip install evdev)
- pygtk for screen size detection (pip install pygtk)
- some things that should be already installed (libusb1.0, uinput) 

## Usage
_$ sudo python pinspiroy.py_

Configuration values are found in config.py. It has settings for rotating axes for left-handed use and disabling the trackpad (I find it gets in the way). The pad buttons are setup to change positions when rotated also.
Added options for simple pressure curves and pressure needed for a full stroke. Defaults are linear pressure and 100% force for full pressure. I'd recommend using your art programs pressure adjustments instead of these options if you can.

For multimonitor setups you will need to update the config file for monitor size and offset of the target screen. Example monitor setup shown below where the tablet is drawing to the monitor on the right. The trackpad controls the same monitor set here.

![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/monitors.png)

Button and gesture bindings are found in bindings.py. Note: If you're adding new keys to your bindings you will have to add them to the virtual button pad capabilities: see 'cap_btn' in pinspiroy.py

## Configuring

I have the button and gesture bindings set up with the following for defaults

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


## Troubleshooting
This program requires the uinput module to be loaded. Either manually (_sudo modprobe uinput_)
or automatically on boot; [see the Arch wiki](https://wiki.archlinux.org/index.php/Kernel_modules).

**Insufficient permissions:** This program requires root access to read USB data (pyusb/libusb). You could add this to your sudoers file to run at start without password entry, but that is not recommended for security reasons.

**Pen not moving on contact, buttons and trackpad working:** This seems to be a problem with libinput requiring a pen resolution; changing the resolution with python-evdev doesn't seem to work. Check that you don't have a libinput driver catchall rule for tablets in your xorg.conf.d/. You may need a evdev driver catchall rule for tablets.

**Key error: NUM:** Run the debug.py file to see the array data the tablet is sending. The first array value should be 8. If it isn't (probably will be 10) the tablet isn't in full tablet mode. See usage section.

Still working out some of the problems, but feel free to tweet @ me or open an issue.

## TODO:
- ~~Figure out USB data to send to the tablet to flip it to full functioning mode so Windows VM not needed~~ thanks to @KaiJan57 for the magic fix
- ~~Add support for tablet in impaired mode~~ no longer needed
- Get stylus buttons working
- Load config file for program-specific bindings
- Add a config GUI
- ~~add configuration for multiple monitors and irregular resolutions~~

![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/spin2.gif)
