'''
Written by Jeang Jenq Loh
Last updated on 5 April 2019

For optimizing roto workflow
Disabled up/down arrow hotkeys so doesn't accidentally change viewer input
Assign 'Q', 'W', 'Alt+Q', 'Alt+W' as previous/next frame/keyframe/increment to Viewer
Option to enable/disable hotkeys so to use its original functions
Now you can keep your hand still in keyboard and tablet while rotoing!

Related docs:
https://support.foundry.com/hc/en-us/articles/115001297930-Q100354-How-to-activate-a-Nuke-menu-command-using-Python
https://doc.qt.io/qt-5/qaction.html
https://learn.foundry.com/nuke/developers/latest/pythonreference/nuke.MenuItem-class.html
'''

import nuke
viewerMenu = nuke.menu('Viewer')

#setting list of items/commands/hotkeys to add and/or remove
labels = ['Next Frame', 'Previous Frame', 'Next Keyframe or Increment', 'Previous Keyframe or Increment']
commands = ['nuke.activeViewer().frameControl(+1)', 'nuke.activeViewer().frameControl(-1)', 'nuke.activeViewer().frameControl(+2)', 'nuke.activeViewer().frameControl(-2)']
hotkeys = ['w', 'q', 'alt+w', 'alt+q']
conflictingLabels = ['Enable Wipe', 'Overlay', 'Set New ROI'] #original items with conflicting hotkeys

#disable up/down arrow hotkeys in viewer
viewerMenu.findItem('Previous Input (A Side)').setEnabled(False)
viewerMenu.findItem('Next Input (A Side)').setEnabled(False)

#Add commands and functions to viewer menu
index = 0
for new in labels:
    viewerMenu.addCommand(new, commands[index])
    index += 1

def enableRotoHotkeys():
    for old in conflictingLabels:
        viewerMenu.findItem(old).setShortcut('')
        #viewerMenu.findItem(old).setEnabled(False)
        print 'disabled ' + old + ' hotkey...'
    index = 0
    for new in labels:
        viewerMenu.findItem(new).setShortcut(hotkeys[index])
        print 'enabled ' + new + ' hotkey...'
        #viewerMenu.findItem(new).setEnabled(True)
        index += 1

def disableRotoHotkeys():
    for roto in labels:
        viewerMenu.findItem(roto).setShortcut('')
        #viewerMenu.findItem(roto).setEnabled(False)
        print 'cleared ' + roto + ' hotkey...'
    index = 0
    for original in conflictingLabels:
        #viewerMenu.findItem(original).setEnabled(True)
        viewerMenu.findItem(original).setShortcut(hotkeys[index])
        print 'enabled ' + original + ' hotkey...'
        index += 1



#Add functions to viewer menu on nuke menu
viewerSubMenu = nuke.menu('Viewer').addMenu('Roto Hotkeys')
viewerSubMenu.addCommand('Enable', "viewerRotoHotkeys.enableRotoHotkeys()", '', icon='Roto.png')
viewerSubMenu.addCommand('Disable', "viewerRotoHotkeys.disableRotoHotkeys()", '')