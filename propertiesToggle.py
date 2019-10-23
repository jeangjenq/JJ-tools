version = 2.0
'''
propertiesToggle

Written by Jeang Jenq Loh
27 April 2019
###########################

showToggle(nodes), '\'
Toggle node floating properties

showConfirmation(nodes)
Confirmation if opening more than 10 properties at a time

toggleInside(), 'Ctrl + \'
Show properties of a node inside a group/gizmo

close(), 'Alt + a'
Close all opened properties, including project settings
'''

import nuke
import nukescripts
import webbrowser


# function to toggle properties (as floating only)
def showToggle(nodes):
    for node in nodes:
        if node.shown():
            node.hideControlPanel()
        else:
            node.showControlPanel(forceFloat=True)


# confirm with user if opening more than 10 floating properties
def showConfirmation(nodes):
    showing = 0
    for node in nodes:
        if not node.shown():
            showing += 1

    if showing < 10:
        showToggle(nodes)
    else:
        confirmation = "This action will open " + str(showing) + ' control panels and may take a long time. Do you want to continue?'
        if nuke.ask(confirmation):
            showToggle(nodes)


# function to toggle properties inside a group/gizmo
def toggleInside():
    # Create drop down python panel to select node
    class toggleInsidePanel(nukescripts.PythonPanel):
        def __init__(self):
            nukescripts.PythonPanel.__init__(self, "Show properties of")
            nodes = []
            for node in nuke.allNodes(group=nuke.selectedNode()):
                nodes.append(node.name())
            self.nodeList = nuke.Enumeration_Knob('showNode', "Show node", nodes)
            self.addKnob(self.nodeList)

        def showModalDialog(self):
            show = nukescripts.PythonPanel.showModalDialog(self)
            if show:
                nameInRoot = nuke.selectedNode().name() + "." + self.nodeList.value()
                showToggle([nuke.toNode(nameInRoot)])

    # If selected node is not a group/gizmo, show node's properties instead
    if 'gizmo_file' in nuke.selectedNode().knobs() or nuke.selectedNode().Class() == 'Group':
        toggleInsidePanel().showModalDialog()
    else:
        showConfirmation(nuke.selectedNodes())


# close all properties and project setting if opened
def close():
    nuke.root().hideControlPanel()
    [node.hideControlPanel() for node in nuke.allNodes(recurseGroups=True)]

# Add to menu and assign shortcut key
propertiesMenu = nuke.menu('Nuke').findItem('Edit/Node').addMenu('Properties')
propertiesMenu.addCommand('propertiesToggle ' + str(version), "webbrowser.open('http://www.nukepedia.com/python/nodegraph/propertiestoggle')")
propertiesMenu.addCommand('Close all properties', 'propertiesToggle.close()', 'alt+a')
propertiesMenu.addCommand('Toggle selected properties', 'propertiesToggle.showConfirmation(nuke.selectedNodes())', '\\')
propertiesMenu.addCommand('Show properties of node inside group\/gizmo', 'propertiesToggle.toggleInside()', 'ctrl+\\')