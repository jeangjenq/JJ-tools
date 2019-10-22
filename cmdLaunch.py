'''
cmdLaunch v1.2
Relaunch Nuke with terminal to display and keep log of error messages.

Added list of terminals, now compatible with different linux distros
'''
import nuke
from os import popen
from platform import system
from distutils.spawn import find_executable

def isNot_exec(name):
    #check whether terminal program exists
    return find_executable(name) is None

def findTerminal():
    termList = ["x-terminal-emulator", "konsole", "gnome-terminal", "urxvt", "rxvt", "termit", "terminator", "Eterm", "aterm", "uxterm", "xterm", "roxterm", "xfce4-terminal", "termite", "lxterminal", "mate-terminal", "terminology", "st", "qterminal", "lilyterm", "tilix", "terminix", "kitty", "guake", "tilda", "alacritty", "hyper"]
    #list taken from https://github.com/i3/i3/blob/next/i3-sensible-terminal
    i = 0
    for term in termList:
        if isNot_exec(term):
            i += 1
        else:
            break
    return termList[i]

def cmdLaunch(XS):

    defineNuke = '"' + nuke.env["ExecutablePath"] + '"'
    if XS == 1:
        defineNuke += " --nukex"
    elif XS == 2:
        defineNuke += " --studio"
    else:
        pass

    if system() == 'Windows':
        startCommand = "start cmd /k "
    elif system() == 'Linux':
        startCommand = findTerminal() + " -e "

    cmdStart = startCommand + defineNuke
    popen(cmdStart)
    nuke.scriptExit()

nodeMenu = nuke.menu('Nuke').findItem('File')
nodeMenu.addCommand('Restart with CMD Terminal/Nuke', 'cmdLaunch.cmdLaunch(0)')
nodeMenu.addCommand('Restart with CMD Terminal/NukeX', 'cmdLaunch.cmdLaunch(1)')
nodeMenu.addCommand('Restart with CMD Terminal/Studio', 'cmdLaunch.cmdLaunch(2)')
