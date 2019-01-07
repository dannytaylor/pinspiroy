# UPDATE, READ FIRST:

**I believe this tablet is supported as of version 9 of the [DIGImend driver](https://github.com/DIGImend/digimend-kernel-drivers) so ths project is no longer required as a work around.**

# pinspiroy

pinspiroy is a linux driver workaround for the [Huion Inspiroy G10T](https://www.huiontablet.com/g10t.html). Note that this is not kernel-level driver, it is a user land implementation that creates virtual devices with uinput to mimic the tablet functionality.

All features of the tablet should be working with this. I'm not too familiar with python so this is likely a non-optimal implementation. Feel free to open an issue or tweet at me if you run into any problems. [@xhiggy](https://twitter.com/xhiggy)

## Requirements
- python2.7
- [pyusb](https://walac.github.io/pyusb/) (pip install pyusb)
- [python-evdev](https://github.com/gvalkov/python-evdev) (pip install evdev)
- [pygtk]() for screen size detection and pinwiz tool (available in via most package managers)

For distros newer than Ubuntu 16.04 you will have to append the following to your `/etc/udev/hwdb.d/61-evdev-local.hwdb` file (create the file if it does not already exist).
```
evdev:name:pinspiroy-pen*
 EVDEV_ABS_00=::5080
 EVDEV_ABS_01=::5080
```
Then run `#sudo systemd-hwdb update` to apply the changes. (thanks to [KaiJan57 for figuring this out](https://github.com/dannytaylor/pinspiroy/issues/6)).


## Usage

```
$ sudo python pinspiroy.py [usersettings.py]
```

If no settings file is given it will load the *default.py* file. Custom settings files must be in the repo folder with a .py extension. Superuser privileges are required to read USB traffic.


## Configuration
Custom configuration can be done via the *pinwiz.py* tool provided. 
```
$ python pinwiz.py
```
It will export a configuration file to the working folder which can be passed to the pinspiroy script when run. The pinwiz tool is very simple with no error checking for invalid settings, so be careful with your inputs and debug the exported file with a text editor if needed.

Default configuration values are found in default.py. It has settings for rotating axes for left-handed use and disabling the trackpad (I find it gets in the way). Disabling the trackpad does not disable the gesture bindings except for the 'taps'. The pad buttons and gestures are setup to change bindings when rotated also.

Simple pressure curves and thresholds can be set in settings file (see default.py for comments), however I'd recommend using your art programs pressure adjustments instead of these options.

The default bindings are set up with the following for defaults. I've set these to best with Krita for my workflow, so you may need to change them depending on your art program and preferences.

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

**Modules not found:** Make sure you're installing the modules with the same version of python you're running the script with.

Still working out some of the problems, but feel free to tweet @ me or open an issue.

## Thanks and Additional Reading
- Thanks [@KaiJan57](https://github.com/KaiJan57) for the magic code to get around the Windows VM requirement and also the hwdb.d fix for recent distros.
- Thanks [@DevinPentecost](https://github.com/DevinPentecost) for general python help
- [event codes for uinput use can be found here](https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h)
- [more event code information found here](https://www.kernel.org/doc/Documentation/input/event-codes.txt)
- [useful tutorial for writing a USB driver with PyUSB](https://www.linuxvoice.com/drive-it-yourself-usb-car-6/)
- [writing a uinput tablet driver in C](http://gerev.github.io/laptop-cintiq/)


![](https://github.com/dannytaylor/pinspiroy/blob/master/docs/spin2.gif)
