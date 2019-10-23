'''
refreshViewer v1.0
Written by Jeang Jenq Loh
Last updated 9th May 2019

Refresh active viewer by duplicate, delete old one and rename/reposition new one to old
Fix bug such as roto toolbar disappearing from viewer interface
'''

import nuke
import nukescripts

def refreshViewer():
    # Acquire original viewer and its active input
    viewer = nuke.activeViewer().node()
    acInput = nuke.activeViewer().activeInput()
    viewerName = viewer.name()
    print('Viewer data recorded.')

    for node in nuke.allNodes():
        node['selected'].setValue(0)
    viewer['selected'].setValue(1)  # Copy viewer only
    nukescripts.node_copypaste()
    print('Viewer duplicated.')

    newViewer = nuke.selectedNode()

    # Set new viewer's inputs to same as old
    inputs = range(viewer.inputs())
    for vInput in inputs:
        newViewer.setInput(vInput, viewer.input(vInput))
    print('Complete setting viewer\'s inputs')

    # Match old viewer's position and delete the old
    newViewer.setXYpos(viewer.xpos(), viewer.ypos())
    nuke.delete(viewer)
    print('Old viewer deleted.')
    # Rename new viewer to original
    newViewer['name'].setValue(viewerName)
    # Set active input to original
    nukescripts.connect_selected_to_viewer(acInput)

# Add to viewer menu
viewerMenu = nuke.menu('Nuke').findItem('Viewer')
viewerMenu.addCommand('Refresh Active Viewer', "refreshViewer.refreshViewer()", '')