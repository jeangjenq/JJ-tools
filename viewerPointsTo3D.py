# Viewer menu to create pointsTo3D node
# Set point 1, 2, 3
import nuke

# Grabbed this function from Hagbarth's QuickCreate
# Return selected midpoint from viewer selection
def viewerSelectedPoint():
	#If the viewer is connected to a node we will use input 0 for ref. Else we just use the viewer itself.
	if nuke.activeViewer().node().input(0):
		myNode = nuke.activeViewer().node().input(0)
		if not nuke.selectedNodes(): #Trying to be smart by assuming that you don't want to add a node to nothing.
			myNode.setSelected(1)
	else:
		myNode = nuke.activeViewer().node()
	bboxinfo = nuke.activeViewer().node()['colour_sample_bbox'].value()    #Get the position info from the colour sample bbox
	aspect = float(myNode.width()*myNode.pixelAspect())/float(myNode.height())  #Calcualte the aspect (thanks Tom van Dop for notifying and Jelmen Palsterman for the correction!)
	cornerA = [(bboxinfo[0]*0.5+0.5)*myNode.width(),(((bboxinfo[1]*0.5)+(0.5/aspect))*aspect)*myNode.height()] #Get the button left corner
	cornerB = [(bboxinfo[2]*0.5+0.5)*myNode.width(),(((bboxinfo[3]*0.5)+(0.5/aspect))*aspect)*myNode.height()] #Get the top right corner
	area_WH = [cornerB[0]-cornerA[0],cornerB[1]-cornerA[1]] #Get the width and height of the bbox
	area_Mid = [cornerA[0]+(area_WH[0]/2),cornerA[1]+(area_WH[1]/2)] #Get the center of the bbox
	return [area_Mid[0], area_Mid[1]]

# Define active PointsTo3D node to affect
def activePointsTo3D():
	# Make a list of all PointsTo3D
	pt3_nodes = []
	active_viewer = nuke.activeViewer().activeInput()
	# Use opened panel to determine which PointsTo3D to affect
	for name in nuke.openPanels():
		node = nuke.toNode(name)
		if node.Class() == "PointsTo3D":
			pt3_nodes.append(node)
	# If there's no PointsTo3D properties open, check if viewer is looking at one
	if len(pt3_nodes) == 0:
		node = nuke.activeViewer().node().input(active_viewer)
		if node.Class() == "PointsTo3D":
			node.showControlPanel()
			pt3_nodes.append(node)
	# If there's still no eligible PointsTo3D, check selected nodes
	if len(pt3_nodes) == 0:
		for node in nuke.selectedNodes():
			if node.Class() == "PointsTo3D":
				node.showControlPanel()
				pt3_nodes.append(node)
	# At this point we're just gonna make one
	if len(pt3_nodes) == 0:
		node = nuke.nodes.PointsTo3D()
		node.setInput(0, nuke.activeViewer().node().input(active_viewer))
		node.showControlPanel()
		nuke.zoom(3, [node.xpos(), node.ypos()])
		pt3_nodes.append(node)
	
	# Return the PointsTo3D nodes list
	return pt3_nodes

def setPoint(index, nodes):
	# First check if there's more than one node in the list
	if len(nodes) > 1:
		if not nuke.ask("This will affect more than one PointsTo3D nodes, continue?"):
			return

	if index == 0:
		point = "pointA"
		ref = "ref_timeA"
	elif index == 1:
		point = "pointB"
		ref = "ref_timeB"
	elif index == 2:
		point = "pointC"
		ref = "ref_timeC"
	for node in nodes:
		node[point].setValue(viewerSelectedPoint())
		node[ref].setValue(nuke.frame())

# Add to viewer menu
viewer_menu = nuke.menu("Viewer")
pt3_menu = viewer_menu.addMenu("PointsTo3D", icon="PointsTo3D.png")
points = ["A", "B", "C"]
for index, point in enumerate(points):
	pt3_menu.addCommand("Set as Point %s" % point, "viewerPointsTo3D.setPoint(%d, viewerPointsTo3D.activePointsTo3D())" % index, icon = "PointsTo3D.png")