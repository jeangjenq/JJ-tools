'''
disableWithGUI v1.0

Toggle selected nodes' based on GUI. Set expression on scanline render 'antialiasing' setting when GUI active.
'''

import nuke

def disableWithGUI():
    #get selected nodes
    d = nuke.selectedNodes()
    for l in d:
        #check if selected node is a Scanline render
        if not l.Class() == "ScanlineRender":
            #Clear 'disable' knob expression if exist
            if l['disable'].hasExpression():
                l['disable'].clearAnimated()
                l['disable'].setValue(0)
            #set expression as $gui
            else:
                l['disable'].setExpression('$gui')
        #if selected node is ScanlineRender, set antialiasing to high when GUI inactive
        else:
            if l['antialiasing'].hasExpression():
                l['antialiasing'].clearAnimated()
                l['antialiasing'].setValue(3)
                l['label'].setValue('')
            else:
                l['antialiasing'].setExpression('$gui?0:3')
                l['label'].setValue('Antialiasing set to high when GUI inactive')

#Add to menu and assign shortcut key
nodeMenu = nuke.menu('Nuke').findItem('Edit/Node')
nodeMenu.addCommand('Custom/Disable selected nodes while GUI is active', 'disableWithGUI.disableWithGUI()', 'alt+d')
