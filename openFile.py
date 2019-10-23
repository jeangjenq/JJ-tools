'''
openFile written by Jeang Jenq Loh
Last update on 22 August 2019

Open selected node's file path, if there's one
Works with gizmos!
Create read node from write node

Update 15 October 2019
    open_read_file() now works with NIM write gizmo

Update August 2019
    Works with Shotgun WriteTank
    Works with SmarVector
'''

import platform
import os
import subprocess
import nuke

def sgtk_write_path():
    try:
        from PySide2 import QtWidgets
    except:
        from PySide import QtGui as QtWidgets
    path = QtWidgets.QApplication.clipboard().text()
    return path

def gather_path(node):
    for knob in node.knobs():
        current_knob = node[knob]
        if current_knob.Class() == 'File_Knob':
            if current_knob.evaluate() is not None:
                return current_knob.evaluate()

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
        # Execute copy path knob if node is ShotgunWriteTank
        if node.Class() == 'WriteTank':
            node['tk_copy_path'].execute()
            if os.path.dirname(sgtk_write_path()) not in read_path:
                read_path.append(os.path.dirname(sgtk_write_path()))
        # If node is gizmo, look for file paths within
        elif 'gizmo_file' in node.knobs():
            for inNode in nuke.allNodes(group=node):
                if gather_path(inNode) is not None:
                    if os.path.dirname(gather_path(inNode)) not in read_path:
                        read_path.append(os.path.dirname(gather_path(inNode)))
        # Else just look for file knob
        else:
            if os.path.dirname(gather_path(node)) not in read_path:
                read_path.append(os.path.dirname(gather_path(node)))

    if read_path is not None:
        if len(read_path) > 4:
            if nuke.ask('About to open ' + str(len(read_path)) + " paths, continue?"):
                for path in read_path:
                    open_folder(path)
        else:
            for path in read_path:
                open_folder(path)

#Create read node from write node
def read_from_write():
    compatibleClass = ['Write', 'WriteTank', 'SmartVector']
    selected = nuke.selectedNodes()
    writeNodes = []
    for node in selected:
        if node.Class() in compatibleClass:
            writeNodes.append(node)
        else:
            hasWrite = False
            for inNode in nuke.allNodes(group=node):
                if inNode.Class() in compatibleClass:
                    hasWrite = True
            if hasWrite:
                writeNodes.append(node)

    if len(writeNodes) < 1:
        nuke.message("Please select a Write node.")
    else:
        writeList = []
        for n in writeNodes:
            writeValues = []
            if n.Class() in compatibleClass:
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
            if write[0].Class() == 'WriteTank':
                write[0]['tk_copy_path'].execute()
                read_path = sgtk_write_path()
            else:
                read_path = nuke.filename(write[0])

            if write[0].Class() == 'SmartVector':
                first_frame = write[0]['file.first_frame'].value()
                last_frame = write[0]['file.last_frame'].value()
            else:
                if write[0]["use_limit"].value() is True:
                    first_frame = write[0]["first"].value()
                    last_frame = write[0]["last"].value()
                else:
                    first_frame = nuke.Root()["first_frame"].value()
                    last_frame = nuke.Root()["last_frame"].value()

            writeNode = nuke.nodes.Read(
                file=read_path,
                first=first_frame,
                last=last_frame,
                origfirst=first_frame,
                origlast=last_frame)
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