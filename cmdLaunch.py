import nuke
import os
import platform

def cmdOpen(XS):

    defineNuke = '"' + nuke.env["ExecutablePath"] + '"'
    if XS == 1:
        defineNuke += " --nukex"
    elif XS == 2:
        defineNuke += " --studio"
    else:
        pass

    if platform.system() == 'Windows':
        startCommand = "start cmd /k "
    elif platform.system() == 'Linux':
        startCommand = "gnome-terminal -x "

    cmdStart = startCommand + defineNuke
    os.popen(cmdStart)
    nuke.scriptExit()

nodeMenu = nuke.menu('Nuke').findItem('File')
nodeMenu.addCommand('Restart with CMD Terminal/Nuke', 'cmdOpen.cmdOpen(0)')
nodeMenu.addCommand('Restart with CMD Terminal/NukeX', 'cmdOpen.cmdOpen(1)')
nodeMenu.addCommand('Restart with CMD Terminal/Studio', 'cmdOpen.cmdOpen(2)')
