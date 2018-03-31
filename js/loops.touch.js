function nodeClickedAsLooper(diagram, node) {
	//log("[nodeClicked] " + nstr(node))

	// === circle nodes are special === //
	if (node.isCenter) {		
		return
	}
		
	// === initial node is special === //
	if (diagram.startNode == null) {
		diagram.startNode = node
		node.looped = true
		node.shape.fill = diagram.currentColor
		var next = null
		var curr = node
		
		var workedNodes = new go.Set() 		
		workedNodes.add(node)
		
		var baseNodes = new go.Set()
		node.cycleCenterNode.cycleChildNodes.each(leaf => {
			baseNodes.addAll(leaf.bases)
		})
		
		for (var i = 0; i < diagram.k3cc; i++) {
			for(var j = 0; j < diagram.k2cc; j++) {
			
				if (next != null) {
					appendPath(diagram, curr, next, true)
					curr = next
					workedNodes.add(curr)
				}
				
				for (var k = 0; k < diagram.k1cc; k++) {
					next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[curr.key])])
					appendPath(diagram, curr, next, true)
					curr = next
					workedNodes.add(curr)
				}
				curr.cycleCenterNode.shape.fill = diagram.currentColor
				curr.cycleCenterNode.cycleChildNodes.each(leaf => {
					baseNodes.addAll(leaf.bases)
				})								
				next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[curr.key])])
			}
			
			next = diagram.findNodeForKey(diagram.pids[D3(diagram.perms[curr.key])])
		}
		
		//workedNodes.each(base => { base.availabled = false; diagram.available_count -= 1 })
		log("initial click pre try")
		tryMakeAvailable(diagram, workedNodes)
		log("initial click done")
//		addAvailables(diagram, node, curr)
		
	} else if (node.availabled && !node.extended) {
		extendAt(diagram, node, true)
	} else if (node.extended) {
		collapseAt(diagram, node, true)
	}
			
	drawNodes(diagram)
		
	return
}

function nodeClickedAsMarker(diagram, node) {
	log("marker begin")
	if (node.isCenter)
		return
		
	node.loopColor = diagram.currentColor
	node.loopBrethren.each(bro => bro.loopColor = diagram.currentColor) 
	
	drawNodes(diagram)
}

function nodeClickedAsBacker(diagram, node) {
	log("backer begin")

	// === circle nodes are special === //
	if (node.isCenter) {		
		var shouldBack = !node.backed
	
//		diagram.nodes.each(node => {
//			node.backed = false
//		})
			
		if (shouldBack) {
			node.backed = true
			var hueSlice = 360 / (diagram.spClass + 1)
			node.backedColorHue = hueSlice
			var hue = hueSlice * 2
			node.cycleCenterNode.cycleChildNodes.each(leaf => {
				leaf.backed = true
				leaf.backedColorHue = hue
				leaf.bases.each(base => {
					base.backed = true
					base.backedColorHue = hue
				})
				hue = (hue + hueSlice) % 360
			})
		} else {
			diagram.nodes.each(node => {
				node.backed = false
			})
		}
		
	} else {
	// === normal nodes are special too === //
		node.backed = true
		node.backedColorHue = 30
		node.potentials.each(leaf => {
//			if(leaf.backed == false) {
				leaf.backed = true
				leaf.backedColorHue = 30
//			}
		})
	}
	
	drawNodes(diagram)
	log("backer done.")
}

function nodeClicked(e, node) {
	var diagram = node.diagram;
	if(diagram.mode == "LOOP")
		nodeClickedAsLooper(diagram, node)
	else if(diagram.mode == "PATH")
		nodeClickedAsPather(diagram, node)
	else if(diagram.mode == "MARK")
		nodeClickedAsMarker(diagram, node)
	else if(diagram.mode == "BACK")
		nodeClickedAsBacker(diagram, node)
}

function extendAt(diagram, node, visual) {
	//log("[extendAt] " + nstr(node) + " (" + visual + ")")
	// extend S2 if S1:S2:S3 to S1:[P:[S]x(𝒮-1)]x(𝒮-2):P:S3
	if (node.prevLink == null
		|| node.prevLink.ctype != 1
		|| node.nextNode == null
		|| node.nextLink.ctype != 1
		|| node.nextNode.nextNode == null
		|| node.nextNode.nextLink.ctype != 1)
		return false
	
	// extend only if available and not already extended	
	if (!node.availabled || node.extended)
		return false
	
	// mark as extended
	node.extended = true
	node.extendedColor = diagram.currentColor

	// should [~] collect brethren nodes from cycle centers
/*	var baseNodes = new go.Set()
	var next = node
	for (var j = 0; j < diagram.spClass - 2; j++) {
		next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[next.key])])		
		next.cycleCenterNode.cycleChildNodes.each(leaf => {
			baseNodes.addAll(leaf.bases)			
		})
		for (var i = 0; i < diagram.spClass - 1; i++) {
			next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[next.key])])					 
		}
	}
*/	
	// add the last node to bases
	var last = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[node.key])])
//	baseNodes.add(last)	
							
	// for all availabled bases, remove availability and potentials
//	makeUnavailable(diagram, baseNodes)
	
	workedNodes = new go.Set()
	
	// delete S2
	deletePath(diagram, node, last, true)
	workedNodes.add(node)
			
	// append extended path
	var curr = node
	for (var j = 0; j < diagram.spClass - 2; j++) {
		next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[curr.key])])
		appendPath(diagram, curr, next, true)
		curr = next
		workedNodes.add(curr)
			
		for (var i = 0; i < diagram.spClass - 1; i++) {
			next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[curr.key])])					 
			appendPath(diagram, curr, next, true)
			curr = next
			workedNodes.add(curr)
		}
	
//		if (visual) {		
			curr.cycleCenterNode.shape.fill = diagram.currentColor
//		}
	}
	
	// append the last P path
	next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[curr.key])])
	appendPath(diagram, curr, next, true)
	workedNodes.add(last)
	
//	if (visual) {
		next.shape.fill = next.cycleCenterNode.shape.fill
//	}
	
	// add availables to the new extension
//	addAvailables(diagram, node.nextNode, last.prevNode)
	
	tryMakeAvailable(diagram, workedNodes)
	
	if (visual) {
		drawNodes(diagram)
	}
	
	return true
}

function collapseAt(diagram, node, visual) {
	//log("[collapseAt] " + nstr(node) + " (" + visual + ")")
	// collapse only if extended
	if (!node.extended)
		return

	// mark as not extended
	node.extended = false
	
	// remove available nodes for the soon to be collapsed extension  
	var last = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[node.key])])
/*	var baseNodes = new go.Set()
	baseNodes.add(last)	
	removeAvailables(diagram, node.nextNode, last.prevNode)*/

	var workedNodes = new go.Set()

	// remove extended path
	var curr = node
	var next = null
	while(curr != last) {
/*		curr.cycleCenterNode.cycleChildNodes.each(leaf => {
			baseNodes.addAll(leaf.bases)		
		})*/
		next = curr.nextNode
		deletePath(diagram, curr, next, true)
		workedNodes.add(curr)
		curr = next
	}
	
	// add the replacement S path
	appendPath(diagram, node, last, true)
	workedNodes.add(last)
//	if (visual) {
		last.shape.fill = last.cycleCenterNode.shape.fill	
//	}
	
	// for all base nodes, if they can be availabled, do it
	tryMakeAvailable(diagram, workedNodes)
	
	if (visual) {
		drawNodes(diagram)
	}
}
