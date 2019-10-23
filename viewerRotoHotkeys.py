'''
Written by Jeang Jenq Loh
Last updated on 13 August 2019

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
commands = ['frameForward()', 'frameBackward()', 'nuke.activeViewer().frameControl(+2)', 'nuke.activeViewer().frameControl(-2)']
hotkeys = ['w', 'q', 'alt+w', 'alt+q']
conflictingLabels = ['Enable Wipe', 'Overlay', 'Set New ROI'] # original items with conflicting hotkeys

#disable up/down arrow hotkeys in viewer
viewerMenu.findItem('Previous Input (A Side)').setEnabled(False)
viewerMenu.findItem('Next Input (A Side)').setEnabled(False)

#Add commands and functions to viewer menu
index = 0
for new in labels:
    viewerMenu.addCommand(new, commands[index])
    viewerMenu.findItem(new).setEnabled(False)
    index += 1

def toggleRotoHotkeys():
    for items in [conflictingLabels, labels]:
        index = 0
        for item in items:
            menuItem = viewerMenu.findItem(item)
            if menuItem.action().isEnabled():
                menuItem.setShortcut('')
                menuItem.setEnabled(False)
            else:
                menuItem.setEnabled(True)
                menuItem.setShortcut(hotkeys[index])
            index += 1



#Add functions to viewer menu on nuke menu
viewerMenu.addCommand('Toggle Roto Hotkeys', "viewerRotoHotkeys.toggleRotoHotkeys()", 'Alt+Shift+R', icon='Roto.png')