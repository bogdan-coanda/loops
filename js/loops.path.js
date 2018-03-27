
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

