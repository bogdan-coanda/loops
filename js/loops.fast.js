var mxlvl = 0

function jk(diagram) {
	var ss = diagram.ss
	log("[jk] lvl: " + ss.lvl + " | node: " + nstr(ss.lvls_node[ss.lvl]) + " | av: " + ss.lvls_availables[ss.lvl].length + " | avIndex: " + ss.lvls_avIndex[ss.lvl] + " | seen: " + ss.seen.count)
	log("[jk] lvls | " + ss.lvls_node.length + "|" + ss.lvls_seen.length + "|" + ss.lvls_availables.length + "|" + ss.lvls_avIndex.length)
	if(ss.lvl >= mxlvl) {
		mxlvl = ss.lvl
		console.log(mxlvl)
	}
	
	if (ss.state == "done.")
		return
	
	if (ss.state == "new") {
		ss.init()
		drawNodes(diagram)
		
		if(diagram.auto) {
			setTimeout(function() {
					jk(diagram)
			}, 1000)
		}
		return
	}				
	
	if((diagram.drawn.availables.length == 0 && diagram.drawn.looped_count != diagram.perms.length) || diagram.drawn.unreachable_cycle_count != 0 || ss.lvls_node[ss.lvl] == null	|| ss.lvls_avIndex[ss.lvl] == ss.lvls_availables[ss.lvl].length) {
		
		if(diagram.drawn.availables.length == 0 && diagram.drawn.looped_count == diagram.perms.length) {
			
			ss.state = "done."
			log("FOUND!!!")
			drawNodes(diagram)
			return // the end
		
		} else {
			// just another dead end ⇒ backtrack one lvl
			ss.pop_lvl()	
			
			if (ss.lvl == -1) { // sanity
				ss.state = "done."				
				log("NOT FOUND?!?")
				drawNodes(diagram)
				return // oh no
			}		
		
			// and clean up previous lvl trial
			collapseFast(diagram, ss.lvls_node[ss.lvl])
			log("[bk] collapsing: " + nstr(ss.lvls_node[ss.lvl]))
			ss.seen.add(ss.lvls_node[ss.lvl])
			ss.lvls_seen[ss.lvl].add(ss.lvls_node[ss.lvl])
			
			// and continue
			ss.next_available()
			
			drawNodes(diagram)

			if (diagram.auto) {
				setTimeout(function() {
					jk(diagram)
				}, 0)
			}
			
			return			
		}
	} 
	
	// else, carry on
	ss.lvls_node[ss.lvl].marked = true
	ss.lvls_node[ss.lvl].markedColor = 'black'
	
	var didExtend = false
	
	if (ss.seen.has(ss.lvls_node[ss.lvl]) == false && extendFast(diagram, ss.lvls_node[ss.lvl])) {
		log("[bk] extending: " + nstr(ss.lvls_node[ss.lvl]))
		
		ss.push_lvl()

		drawNodes(diagram)

		if(diagram.auto) {						
			setTimeout(function() {
				jk(diagram)
			}, 20)
		}
			
	} else {
		// or continue
		ss.next_available()
					
		drawNodes(diagram)
		
		if(diagram.auto) {
			setTimeout(function() {
				jk(diagram)
			}, 0)
		}
	}
}

function bk(diagram, lvl, seen) {
	log("[bk] lvl: " + lvl + " | seen: " + seen.count)
	if(lvl >= mxlvl) {
		mxlvl = lvl
		console.log(mxlvl)
	}
	var node = diagram.startNode
	var cc = 0
	var av = 0
	var lvlseen = new go.Set()
	
	while (node != null) {
		cc += 1
		if (seen.has(node) == false && extendFast(diagram, node)) {
			log("[bk] extending: " + nstr(node))
			av += 1
			if(bk(diagram, lvl+1, seen))
				return true
			collapseFast(diagram, node)
			log("[bk] collapsing: " + nstr(node))
			seen.add(node)
			lvlseen.add(node)
		}
		node = node.nextNode
	}
	if(av == 0 && cc == diagram.perms.length) {
		log("FOUND!!!")
		drawNodes(diagram)
		return true
	}
	
	// [~] need to remove the current lvl seens
	seen.removeAll(lvlseen)
	
	return false	
}

function extendFast(diagram, node) {
	//log("[extendAt] " + nstr(node) + " (" + visual + ")") 
	// extend S2 if S1:S2:S3 to S1:[P:[S]x(ss-1)]x(ss-2):P:S3
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

	// add the last node to bases
	var last = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[node.key])])
//	baseNodes.add(last)	
							
	// for all availabled bases, remove availability and potentials
//	makeUnavailable(diagram, baseNodes)
	
	workedNodes = new go.Set()
	
	// delete S2
	deleteFast(diagram, node, last)
	workedNodes.add(node)
			
	// append extended path
	var curr = node
	for (var j = 0; j < diagram.spClass - 2; j++) {
		next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[curr.key])])
		appendFast(diagram, curr, next)
		curr = next
		workedNodes.add(curr)
			
		for (var i = 0; i < diagram.spClass - 1; i++) {
			next = diagram.findNodeForKey(diagram.pids[D1(diagram.perms[curr.key])])					 
			appendFast(diagram, curr, next)
			curr = next
			workedNodes.add(curr)
		}
	
//		if (visual) {		
			curr.cycleCenterNode.shape.fill = diagram.currentColor
//		}
	}
	
	// append the last P path
	next = diagram.findNodeForKey(diagram.pids[D2(diagram.perms[curr.key])])
	appendFast(diagram, curr, next)
	workedNodes.add(last)
	
//	if (visual) {
		next.shape.fill = next.cycleCenterNode.shape.fill
//	}
	
	// add availables to the new extension
//	addAvailables(diagram, node.nextNode, last.prevNode)
	
	tryMakeAvailableFast(diagram, workedNodes)
	
	return true
}

function collapseFast(diagram, node) {
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
		deleteFast(diagram, curr, next)
		workedNodes.add(curr)
		curr = next
	}
	
	// add the replacement S path
	appendFast(diagram, node, last)
	workedNodes.add(last)
//	if (visual) {
		last.shape.fill = last.cycleCenterNode.shape.fill	
//	}
	
	// for all base nodes, if they can be availabled, do it
	tryMakeAvailableFast(diagram, workedNodes)
}

function appendFast(diagram, curr, next) {
	curr.nextNode = next
	next.prevNode = curr
	
	next.looped = true
	next.shape.fill = diagram.currentColor
	
	next.findLinksInto().each(link => { 
		if (link.fromNode == curr) {
			curr.nextLink = next.prevLink = link
			link.commited = true
			link.part.opacity = 1
			link.part.zOrder = 100					
		}
	})
}

function deleteFast(diagram, curr, next) {
	curr.nextNode = null
	next.prevNode = null
	
	next.looped = false
	next.extended = false
	next.shape.fill = "white"
		
	next.findLinksInto().each(link => { 
		if (link.fromNode == curr) {
			curr.nextLink = next.prevLink = null
			link.commited = false
			link.part.opacity = 0
			link.part.zOrder = 0
		}
	})
}

function tryMakeAvailableFast(diagram, nodes) {
	nodes.each(node => {
		wasAvailabled = node.availabled
		if (node.availabled = checkAvailabilityFast(diagram, node)) {
			if (wasAvailabled == false)
				diagram.available_count += 1
			node.loopBrethren.each(bro => bro.availabled = true)
		} else {
			if (wasAvailabled == true)
				diagram.available_count -= 1
			node.loopBrethren.each(bro => bro.availabled = false)
		}
	})
}

function checkAvailabilityFast(diagram, curr) {
	if(curr.looped && (
		curr.prevLink == null
		|| curr.prevLink.ctype != 1 
		|| curr.nextNode == null 
		|| curr.nextLink.ctype != 1 
		|| curr.nextNode.nextNode == null 
		|| curr.nextNode.nextLink.ctype != 1))
		return false

	return curr.loopBrethren.filter(bro => bro.looped).count + (curr.looped ? 1 : 0) <= 1
}

