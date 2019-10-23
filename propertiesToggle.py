'''
propertiesToggle v1.0

Written by Jeang Jenq Loh
22 March 2019
###########################

showToggle(), ','
Toggle node floating properties

showConfirmation()
Confirmation if opening more than 10 properties at a time

close(), 'Alt + a'
Close all opened properties, including project settings

'''

import nuke

#function to toggle properties (as floating only)
def showToggle():
    for node in nuke.selectedNodes():
        if node.shown():
            node.hideControlPanel()
        else:
            node.showControlPanel(forceFloat=True)

#confirm with user if opening more than 10 floating properties
def showConfirmation():
    showing = 0
    for node in nuke.selectedNodes():
        if not node.shown():
            showing += 1

    if showing > 10:
        confirmation = "This action will open " + str(showing) + ' control panels and may take a long time. Do you want to continue?'
        if nuke.ask(confirmation):
            showToggle()
    else:
        showToggle()

#close all properties and project setting if opened
def close():
    nuke.root().hideControlPanel()
    [node.hideControlPanel() for node in nuke.allNodes(recurseGroups=True)]

#Add to menu and assign shortcut key
nuke.menu('Nuke').findItem('Edit').addCommand('Close all properties', 'closeProperties.close()', 'alt+a')
nuke.menu('Nuke').findItem('Edit').addCommand('Toggle selected properties', 'closeProperties.showConfirmation()', ',')