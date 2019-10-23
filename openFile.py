'''
openFile written by Jeang Jenq Loh
Last update on 27 April 2019

Open selected node's file path, if there's one
Works with gizmos!
Create read node from write node
'''

import platform
import os
import subprocess
import nuke
import nukescripts

#Open path's folder
def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(os.path.abspath(path))
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    elif platform.system() == "Linux":
        subprocess.check_call(["xdg-open", path])
    else:
        nuke.message("Unsupported OS")

#Open selected node's folder
def open_read_file():
    read_path = []
    for node in nuke.selectedNodes():
        for knob in node.knobs():
            current_knob = node[knob]
            if current_knob.Class() == 'File_Knob':
                if current_knob.evaluate() is not None:
                    if os.path.dirname(current_knob.evaluate()) not in read_path:
                        read_path.append(os.path.dirname(current_knob.evaluate()))
    if len(read_path) > 4:
        if nuke.ask('About to open ' + str(len(read_path)) + " paths, continue?"):
            for path in read_path:
                open_folder(path)
    else:
        for path in read_path:
            open_folder(path)

#Create read node from write node
def read_from_write():
    selected = nuke.selectedNodes()
    writeNodes = []
    for node in selected:
        if node.Class() == 'Write':
            writeNodes.append(node)
        else:
            hasWrite = False
            for inNode in nuke.allNodes(group=node):
                if inNode.Class() == 'Write':
                    hasWrite = True
            if hasWrite:
                writeNodes.append(node)

    if len(writeNodes) < 1:
        nuke.message("Please select a Write node.")
    else:
        writeList = []
        for n in writeNodes:
            writeValues = []
            if n.Class() == 'Write':
                writeValues.append(n)
                writeValues.append(n.xpos())
                writeValues.append(n.ypos())
                writeList.append(writeValues)
            else:
                for inGroup in nuke.allNodes(group=n):
                    if inGroup.Class() == 'Write':
                        writeValues.append(inGroup)
                        writeValues.append(n.xpos())
                        writeValues.append(n.ypos())
                        writeList.append(writeValues)

        for write in writeList:
            if write[0]["use_limit"].value() is True:
                first_frame = write[0]["first"].value()
                last_frame = write[0]["last"].value()
            else:
                first_frame = nuke.Root()["first_frame"].value()
                last_frame = nuke.Root()["last_frame"].value()

            writeNode = nuke.nodes.Read(
                file=nuke.filename(write[0]),
                first=first_frame,
                last=last_frame,
                origfirst=nuke.Root()["first_frame"].value(),
                origlast=nuke.Root()["last_frame"].value())
            writeNode.setXpos(write[1]+100)
            writeNode.setYpos(write[2])

def open_script_folder():
    script = nuke.root()['name'].value()
    if script:
        open_folder(os.path.dirname(script))
    else:
        nuke.message("Nuke script not saved")

nuke.menu('Nuke').findItem('Edit/Node').addCommand('Open node\'s folder', 'openFile.open_read_file()', 'e')
nuke.menu('Nuke').findItem('Edit/Node').addCommand('Create read from write', 'openFile.read_from_write()', '+r')
nuke.menu('Nuke').findItem('File').addCommand('Open nuke script folder', 'openFile.open_script_folder()', '+o')