# Get the last letter/section from node name, separated by "_":
nuke.thisNode().name().rsplit("_").__getitem__(2)

# From the above, can be modified to acquire file extension
nuke.thisNode()['file'].getValue().rsplit(".").__getitem__(2)

# Set expression with python found in the link below, especially useful when setting expression to a dropdown menu which is usually not accessible
# http://nuke.yellow-ant.net/set-expression-via-python/
nuke.selectedNode()['antialiasing'].setExpression('$gui? 0:3')

# List of all nodes but exclude selected ones:
n = nuke.allNodes()
for i in nuke.selectedNodes():
    n.remove(i)
    return n

# Replace frame paddings (%04d) and extension with .mov
import re
v = nuke.toNode('Read1')['file'].value()
print re.sub(r'%.*d.exr', 'mov', v)

# Search for frame paddings
f = nukescripts.replaceHashes(nuke.filename(n))
padd = re.search(r'%.*d', f) print padd.group(0)

# Check if program exist from python script
shutil.which

# Above was introduced in Python 3.3 and is cross-platform, supporting Linux, Mac, and Windows. It is also available in Python 2.x via whichcraft.
def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None

# python2 method to check if program exists
def is_tool(name):
    """Check whether `name` is on PATH."""

    from distutils.spawn import find_executable

    return find_executable(name) is not None

# Get working directory in python
import os
print os.getcwd()

# Check if variable not equal to multiple things
while choice not in [1, 2, 3]:

# Get filename from path
import os

#Get filename with extension
name = os.path.basename(path)
#filename without extension
os.path.splitext(name)[0] #extension is [1]

# Check if node is gizmo
print 'gizmo_file' in nuke.selectedNode().knobs()

# Get list of nodes inside selected gizmo
nodes = nuke.allNodes(group=nuke.selectedNode())

# Automatically populate read nodes frame range and other settings
node = nuke.createNode('Read')
node['file'].fromUserText(path)

# Delayed menu creation
QtCore.QTimer.singleShot(0, lambda: nukemenu.addMenu(menu))