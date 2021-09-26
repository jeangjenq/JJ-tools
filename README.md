# JJ-tools
This is my python library I wrote for The Foundry's Nuke. Most of these scripts are available on Nukepedia and I will link them below. Although Nukepedia might not have the latest versions as I can forget to update them.

## [ffmpeg_write](https://github.com/jeangjenq/ffmpeg_write)
Available on [Nukepedia](http://www.nukepedia.com/gizmos/image/ffmpeg_write)

A custom node that launches ffmpeg and convert sequences.

## [LensKernelFFT](https://github.com/jeangjenq/LensKernelFFT)
[LensKernelFFT] created by Bob Roesler. I made some slight QoL improvements.

## [read_tools](https://github.com/jeangjenq/read_tools)
Available on [Nukepedia](http://www.nukepedia.com/python/misc/read_tools)

A collection of scripts that makes bulk changes to read nodes.

## [setProjDir](https://github.com/jeangjenq/setProjDir)
Available on [Nukepedia](http://www.nukepedia.com/python/misc/setprojdir)

Set project directory and automatically swap out the file paths to relative if you already have file knobs in your script.

## [cmdExecute](./cmdExecute.py)
Available on [Nukepedia](http://www.nukepedia.com/python/render/cmdexecute)

Simple pop up interface to execute a node with terminal. There are plenty other scripts on Nukepedia that launches terminal to render node. 
But I wanted a really quick one without extra features or customization, just click and render with the most basic settings.
And this is it.
Click "F6" with any following node class and it'll launch a simple interface to launch a terminal render.
```python
['Write', 'DeepWrite', 'WriteGeo', 'WriteTank', 'SmartVector']:
```
![render window](http://www.nukepedia.com/images/users/jeangjenq/CMDexecute_interface.png)

## [cmdLaunch](./cmdLaunch.py)
Available on [Nukepedia](http://www.nukepedia.com/python/misc/cmdlaunch)

Relaunch Nuke from cmd/terminal and keep your error messages.

This is a fun one. Launching Nuke from Windows will launch a terminal log along with it, while in Linux there's no log at all. 
A terminal log with all the error messages are great for troubleshooting, unfortunately if Nuke crashes, the log closes along with it after a short delay.
This script relaunch Nuke using Command Prompt or one of your installed linux terminal.
Since it's not part of Nuke's process, if Nuke crashes the terminal stays up and you can read through the log and close it after.

## [disableWithGUI](./disableWithGUI)
While $gui expression can be annoying to someone else working on your script, it is a good trick to speed up responsiveness of your node graph while working on a large script.
This script is assigned to "Alt + D" to add/remove "$gui" expression on selected nodes.
If the selected nodes are scanline renderer, it adds expression to the "anti-aliasing" knob instead, turning AA off while GUI active and high when GUI inactive.

## [frameServerStatus](./frameServerStatus.py)
Available on [Nukepedia](http://www.nukepedia.com/python/ui/frameserverstatus)

A python panel to display currently running frame server slaves.

I wrote this as part of my learning process looking into frameserver and creating a python panel. 
It has the basic function of showing your running slaves, I'm hoping to add more functions to it in the future.
![frameServerStatus panel](http://www.nukepedia.com/images/users/jeangjenq/frameServerUI.PNG)

## [openFile](./openFile.py)




