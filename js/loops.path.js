
/*
function updateArrowCount(link, diagram) {
	var arrowType = link.part.data.width / 2
	diagram.arrowCount[arrowType] += link.commited ? 1 : -1
	document.getElementById("D"+arrowType+"_count").value = diagram.arrowCount[arrowType]
}*/

function appendPath(diagram, curr, next, visual) {
	curr.nextNode = next
	next.prevNode = curr
	
	next.looped = true
	if (visual) {
		next.shape.fill = diagram.currentColor
	}
	
	next.findLinksInto().each(link => { 
		if (link.fromNode == curr) {
			curr.nextLink = next.prevLink = link
			if (visual) {
				link.commited = true
				link.part.opacity = 1
				link.part.zOrder = 100					
			}
		}
	})
}

function deletePath(diagram, curr, next, visual) {
	curr.nextNode = null
	next.prevNode = null
	
	next.looped = false
	next.extended = false
	
	if (visual) {
		next.shape.fill = "white"
	}
		
	next.findLinksInto().each(link => { 
		if (link.fromNode == curr) {
			curr.nextLink = next.prevLink = null
			if (visual) {
				link.commited = false
				link.part.opacity = 0
				link.part.zOrder = 0
			}
		}
	})
}

function extendForMaxAvailability(diagram) {
	var curr = diagram.startNode

	var max_available_count = 0
	var max_available_node = null

	while (curr != null) {
		if (extendAt(diagram, curr, false)) {
			if (diagram.available_count > max_available_count) {
				max_available_count = diagram.available_count
				max_available_node = curr
			}
			collapseAt(diagram, curr, false)
		}
		
		curr = curr.nextNode
	}
	
	extendAt(diagram, max_available_node, true)
	drawNodes(diagram)
}

function extendForMaxPotentiality(diagram) {
	var curr = diagram.startNode

	var max_potential_count = 0
	var max_potential_node = null

	while (curr != null) {
		if (extendAt(diagram, curr, false)) {			
			if (diagram.potential_count > max_potential_count) {
				max_potential_count = diagram.potential_count
				max_potential_node = curr
			}
			collapseAt(diagram, curr, false)
		}
		
		curr = curr.nextNode
	}
	
	extendAt(diagram, max_potential_node, true)
	drawNodes(diagram)
}

function extendForMinAPRatio(diagram) {
	var curr = diagram.startNode

	var min_ap_ratio = 1000
	var min_ap_node = null

	while (curr != null) {
		if (extendAt(diagram, curr, false)) {
			if (diagram.available_count / diagram.potential_count < min_ap_ratio) {
				min_ap_ratio = diagram.available_count / diagram.potential_count
				min_ap_node = curr
			}
			collapseAt(diagram, curr, false)
		}
		
		curr = curr.nextNode
	} 
	
	extendAt(diagram, min_ap_node, true)
	drawNodes(diagram)
}

function checkAvailability(diagram, curr) {
	if(curr.looped && (
		curr.prevLink == null
		|| curr.prevLink.ctype != 1 
		|| curr.nextNode == null 
		|| curr.nextLink.ctype != 1 
		|| curr.nextNode.nextNode == null 
		|| curr.nextNode.nextLink.ctype != 1))
		return false

	return curr.loopBrethren.filter(bro => bro.looped).count + (curr.looped ? 1 : 0) <= 1

	var next = curr
	for (var j = 0; j < diagram.spClass - 2; j++) {
		next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[next.key])])
		if (next.looped == true)
			return false
		
		for (var i = 0; i < diagram.spClass - 1; i++) {
			next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[next.key])])					 
			if (next.looped == true)
				return false
		}
	}
			
	return true
}

function makeUnavailable(diagram, bases) {
	bases.each(base => { if(base.availabled) {
		base.availabled = false
		diagram.available_count -= 1
		updatePotentials(diagram, base, false)
	}})
}

function tryMakeAvailable(diagram, nodes) {

	nodes.each(node => {
		wasAvailabled = node.availabled
		if (node.availabled = checkAvailability(diagram, node)) {
			if (wasAvailabled == false)
				diagram.available_count += 1
			node.loopBrethren.each(bro => bro.availabled = true)
		} else {
			if (wasAvailabled == true)
				diagram.available_count -= 1
			node.loopBrethren.each(bro => bro.availabled = false)
		}
	})
	
	return

	bases.each(base => { if (base.availabled == false) {
		if(base.availabled = checkAvailability(diagram, base)) {
			diagram.available_count += 1
			updatePotentials(diagram, base, true)
		}
	}})
}

function addAvailables(diagram, fromNode, toNode) {
	//log("[addAvailables] from " + nstr(fromNode) + " to " + nstr(toNode))
	var curr = fromNode
	var next = null
		
	while (curr != toNode && curr != null) {
		if (curr.availabled == false) {
			if (curr.availabled = checkAvailability(diagram, curr)) {
				diagram.available_count += 1
	
				// update potentials
				updatePotentials(diagram, curr, true)			
			}
		}
		curr = curr.nextNode
	}	
}

function removeAvailables(diagram, fromNode, toNode) {
	//log("[removeAvailables] from " + nstr(fromNode) + " to " + nstr(toNode))
	var curr = fromNode
	var next = null
				
	while (curr != toNode && curr != null) {
		if(curr.availabled) {
			curr.availabled = false
			diagram.available_count -= 1
							
			// update potentials
			updatePotentials(diagram, curr, false)
		}

		curr = curr.nextNode
	}
}

function updatePotentials(diagram, node, potentialed) {
	// console.log("[updatePotentials] node: " + node.key)
	// updates the next [P:[S]x(𝒮-1)]x(𝒮-2) nodes to potentialedBy 'node'
	var ppc = 0
	var npc = 0
	var pby = 0
	var nby = 0
	
	next = node
	for (var j = 0; j < diagram.spClass - 2; j++) {
		next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[next.key])])
				
		if (potentialed) {
		
			if (next.potentialedBy.has(node.key) == false) {
				if (next.potentialedBy.size == 0) {
					diagram.potential_count += 1
					ppc += 1
					//log("[updatePotentials] ++ for " + nstr(next))
				}
				next.potentialedBy.add(node.key)
				pby += 1
				//log("[updatePotentials] " + nstr(next) + " (+) potentialed by " + nstr(node))				
			}
			
			for (var i = 0; i < diagram.spClass - 1; i++) {
				next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[next.key])])		
				if (next.potentialedBy.has(node.key) == false) {
					if (next.potentialedBy.size == 0) {
						diagram.potential_count += 1
						ppc += 1
						//log("[updatePotentials] ++ for " + nstr(next))
					}
					next.potentialedBy.add(node.key)
					pby += 1
					//log("[updatePotentials] " + nstr(next) + " (+) potentialed by " + nstr(node))				
				}
			}
			
		} else {

			if (next.potentialedBy.has(node.key) == true) {
				next.potentialedBy.delete(node.key)
				nby += 1
				//log("[updatePotentials] " + nstr(next) + " (-) potentialed by " + nstr(node))				
				if (next.potentialedBy.size == 0) {
					diagram.potential_count -= 1
					npc += 1
					//log("[updatePotentials] -- for " + nstr(next))
				}
			}
								
			for (var i = 0; i < diagram.spClass - 1; i++) {
				next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[next.key])])
				if (next.potentialedBy.has(node.key) == true) {
					next.potentialedBy.delete(node.key)
					nby += 1
					//log("[updatePotentials] " + nstr(next) + " (+) potentialed by " + nstr(node))				
					if (next.potentialedBy.size == 0) {
						diagram.potential_count -= 1
						npc += 1
						//log("[updatePotentials] -- for " + nstr(next))
					}
				}
			}			
		}
	}
	//log("[updatePotentials] called for: " + potentialed + " on " + nstr(node) + " | added " + ppc + " by " + pby + " | removed " + npc + " by " + nby)
}
