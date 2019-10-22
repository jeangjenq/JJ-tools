#cmdExecute written by Jeang Jenq Loh
#Last upadted: 28 March 2019
#Version: 1.4

'''
Written as a simple popup interface to quickly execute nodes with a terminal
Default shortcut: F6
Shortcut can be changed at the end of script

Update log:
1.4
Added support for different linux distro terminals, will attempt to find working terminal from list in findTerminal()
Option to use nuke_r license, default is set to use nuke_i

1.3
Added support for linux

1.1 Removed particleCache from executable list
'''

import nuke, nukescripts
import os
import multiprocessing
import platform
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

def cmdExecute():
    Nwrite = nuke.selectedNode()
    NName = Nwrite['name'].value()
    fRange = nuke.activeViewer().node()['frame_range'].getValue()

    #Get list of available CPU threads
    actThd = multiprocessing.cpu_count()
    thds = ""
    thd = range(1, actThd+1)
    for n in thd:
        thds += str(n) + " "

    #Check if selected node is executable
    if Nwrite.Class() not in ['Write', 'DeepWrite', 'WriteGeo', 'WriteTank', 'SmartVector']:
        nuke.message('Selected node is not executable via CMD!') #making sure selected node is executable
    else:
        i = nuke.Panel('cmdExecute v1.4: Render settings')
        i.addSingleLineInput('first', nuke.root().firstFrame())
        i.addSingleLineInput('last', nuke.root().lastFrame())
        i.addEnumerationPulldown('threads', thds)
        i.addBooleanCheckBox('Save new version', 0)
        i.addBooleanCheckBox('Use interactive license', 1)
        i.addBooleanCheckBox('NukeX', 0)
        i.addBooleanCheckBox('Close Nuke', 0)
        if i.show():
            try:
                nuke.scriptSave("")
                ret = [int(i.value('first')), int(i.value('last'))]
                rThd = int(i.value('threads'))
                sav = i.value('Save new version')
                X = i.value('NukeX')
                L = i.value('Use interactive license')
                nukeQuit = i.value('Close Nuke')

                args = '"' + nuke.env["ExecutablePath"] + '"'
                if X:
                    args += "  --nukex"
                if L:
                    args += " -i"
                args += " -m " + str(rThd) \
                        + " -X " + NName \
                        + " -F " + str(ret[0]) + '-' + str(ret[1]) \
                        + " " + '"' + nuke.scriptName() + '"' #Quote unquote for spaces in BAT


                #identify OS
                if platform.system() == "Windows":
                    startCMD = "start cmd /k " + '"' + args + '"' #Quote unquote in case both paths have spaces
                if platform.system() == "Linux":
                    startCMD = findTerminal() + " -e " + args + ' && read line'#Quote unquote in case both paths have spaces
                os.popen(startCMD)
                print "Sending command..."
                print startCMD
                print "Command sent!"

                #save new version
                if sav:
                    nukescripts.script_and_write_nodes_version_up()

                #quit
                if nukeQuit:
                    nuke.scriptExit()

            except:
                nuke.message('Invalid input')

#Add to menu and assign shortcut key
nodeMenu = nuke.menu('Nuke').findItem('Render')
nodeMenu.addCommand('Execute using Command Prompt', 'cmdExecute.cmdExecute()', 'F6')
