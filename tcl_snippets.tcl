# Get input node name
[value this.input0.name][python nuke.thisNode().input(0).name()]

# Set a variable in expression with TCL:
[set VARIABLENAME VALUE; return]

# Use a variable
$VARIABLENAME

# String Operation that return the 5th character from top input name
[string index [value [topnode this.input0].name] 5]

# String Operation that convert string to lowercase
[string tolower [value]]

# Check if anything is plugged into inpu
[exists this.input0]]if nuke.thisNode().input(0) 

# Check if anything is plugged into input 1
[value [topnode this.input0].name][exists parent.[string tolower [value [topnode this.input1].name]]]

# This handy getting filename from topmost read I grabbed from [Nukepedia](http://www.nukepedia.com/tcl/write-nodes-filename-from-topmost-read)
[lindex [split [lindex [split [knob [topnode].file] .] 0] /] end][file dirname [knob [topnode].file]]/[lindex [split [lindex [split [knob [topnode].file] .] 0] /] end]_conv.%04d.exr 

# Get nuke script base name without file extension
[lindex [split [file rootname [python nuke.root().knob('name').value()]] /] end]

# Read metadata with TCL
[metadata input/filename]

# Using expressions in Text node (needs to square bracket the whole thing):
[expression frame==1?1:0]

# Get Bezier1's point 0 (which is first point) position in Roto1 node :
[value Roto1.curves.Bezier1.curve_points.0.main]
