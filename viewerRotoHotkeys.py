'''
print nuke.menu('Viewer').findItem('Overlay')
https://support.foundry.com/hc/en-us/articles/115001297930-Q100354-How-to-activate-a-Nuke-menu-command-using-Python
https://doc.qt.io/qt-5/qaction.html
https://learn.foundry.com/nuke/developers/latest/pythonreference/nuke.MenuItem-class.html
'''

import nuke
viewerMenu = nuke.menu('Viewer')

#disable up/down arrow hotkeys in viewer
viewerMenu.findItem('Previous Input (A Side)').setEnabled(False)
viewerMenu.findItem('Next Input (A Side)').setEnabled(False)

#setting list of items/commands/hotkeys to add and/or remove
labels = ['Next Frame', 'Previous Frame', 'Next Keyframe or Increment', 'Previous Keyframe or Increment']
commands = ['nuke.activeViewer().frameControl(+1)', 'nuke.activeViewer().frameControl(-1)', 'nuke.activeViewer().frameControl(+2)', 'nuke.activeViewer().frameControl(-2)']
hotkeys = ['w', 'q', 'alt+w', 'alt+q']
conflictingLabels = ['Enable Wipe', 'Overlay', 'Set New ROI'] #original items with conflicting hotkeys

#check if items already exist
def itemsExist():
    if viewerMenu.findItem(labels[0]):
        exist = True
    else:
        exist = False
    return exist

def enableRotoHotkeys():
    if not itemsExist():
        print 'rotoHotkeys not detected, adding...'
        for old in conflictingLabels:
            viewerMenu.findItem(old).setShortcut('')
            viewerMenu.findItem(old).setEnabled(False)
        index = 0
        for new in labels:
            viewerMenu.addCommand(new, commands[index], hotkeys[index])
            index += 1
    else:
        for old in conflictingLabels:
            viewerMenu.findItem(old).setShortcut('')
            viewerMenu.findItem(old).setEnabled(False)
        index = 0
        for new in labels:
            viewerMenu.findItem(new).setShortcut(hotkeys[index])
            viewerMenu.findItem(new).setEnabled(True)
            index += 1

def disableRotoHotkeys():
    if itemsExist():
        print 'rotoHotkeys detected, removing...'
        for roto in labels:
            viewerMenu.findItem(roto).setShortcut('')
            viewerMenu.findItem(roto).setEnabled(False)
        index = 0
        for original in conflictingLabels:
            viewerMenu.findItem(original).setEnabled(True)
            viewerMenu.findItem(original).setShortcut(hotkeys[index])
            index += 1



#Add functions to viewer menu on nuke menu
viewerTopMenu = nuke.menu('Nuke').findItem('Viewer')
viewerTopMenu.addCommand('Roto Hotkeys/Enable', "viewerRotoHotkeys.enableRotoHotkeys()", '')
viewerTopMenu.addCommand('Roto Hotkeys/Disable', "viewerRotoHotkeys.disableRotoHotkeys()", '')