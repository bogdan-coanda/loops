function init() {
	var $ = go.GraphObject.make; // for conciseness in defining templates

	log("init()!!!")

	myDiagram = $(go.Diagram, "myDiagramDiv", {
		initialAutoScale: go.Diagram.Uniform,
		padding: 10,
		contentAlignment: go.Spot.Center,
		layout: $(go.Layout, { 
			isInitial: false, 
			isOngoing: false 
		}),
		maxSelectionCount: 1
	});
	
	// define the Node template
	myDiagram.nodeTemplate =
		$(go.Node, "Spot", {
				locationSpot: go.Spot.Center,	// Node.location is the center of the Shape
				locationObjectName: "SHAPE",
				selectionAdorned: false,
				//selectionChanged: nodeSelectionChanged,
				click: nodeClicked
			},
			new go.Binding("location", "loc"),
			$(go.Panel, "Auto",
				$(go.Shape, "Ellipse", { 
						name: "SHAPE",
						fill: "lightgray",	// default value, but also data-bound
						stroke: "black",	// modified by highlighting
						strokeWidth: 1,
						desiredSize: new go.Size(96, 96),
						portId: ""	// so links will go to the shape, not the whole node
					}
				)
			),
			$(go.TextBlock, {
					name: "LABEL",
					font: "italic 700 16px sans-serif", 
					textAlign: "center",
					stroke: "black" 
				},
				new go.Binding("text")
			)
		);

	// define the Link template
	myDiagram.linkTemplate =
		$(go.Link, {
				selectable: false,			// links cannot be selected by the user
				curve: go.Link.Bezier,
				layerName: "Background"	// don't cross in front of any nodes
			},
			$(go.Shape, {
					name: "LINE", 
					stroke: "white"
				},
				new go.Binding("stroke", "color"),
				new go.Binding("strokeWidth", "width")
			),
			$(go.Shape, { 
					name: "ARROW", 
					toArrow: "Standard",
					stroke: "white"
				},
				new go.Binding("stroke", "color"),
				new go.Binding("strokeWidth", "width")
			)
		);
	log("xk")
	myDiagram.startPerm = generateGraph();
	log("xk")
	myDiagram.startNode = null;
	myDiagram.mode = "LOOP"
	myDiagram.currentColor = "yellow"
	myDiagram.currentColor = 60
	myDiagram.arrowCount = [0, 0, 0]
	myDiagram.available_count
	
	myDiagram.auto = true
	myDiagram.ss = {
		state: "new",
		lvl: 0, 
		seen: new go.Set(), 
		lvls_node: [null], 
		lvls_seen: [new go.Set()], 
		lvls_availables: [[]], 
		lvls_avIndex: [0],
		lvls_hasSingles: [false],
		
		init: function() {
			this.state = "running"
	
			drawNodes(myDiagram)
				
			this.lvls_node = [myDiagram.drawn.availables[0]]
			this.lvls_node[0].marked = true
			this.lvls_node[0].markedColor = 'black'
			this.lvls_availables = [myDiagram.drawn.availables]
			this.lvls_hasSingles = [myDiagram.drawn.singles.size > 0]
		},
		next_available: function() {
			this.lvls_node[this.lvl].marked = false
			this.lvls_avIndex[this.lvl] = this.lvls_avIndex[this.lvl] + 1
			if (this.lvls_hasSingles[this.lvl] == false && this.lvls_avIndex[this.lvl] < this.lvls_availables[this.lvl].length) {
				this.lvls_node[this.lvl] = this.lvls_availables[this.lvl][this.lvls_avIndex[this.lvl]]
				this.lvls_node[this.lvl].marked = true
				this.lvls_node[this.lvl].markedColor = 'black'
			} else {
				this.lvls_node[this.lvl] = null
			}
		},
		push_lvl: function() {

			this.lvls_node[this.lvl].marked = false
			//this.lvls_node[this.lvl].markedColor = 'gray'
		
			this.lvl += 1
			myDiagram.currentColor = hsl((15*this.lvl) % 360)			
			this.lvls_seen.push(new go.Set())

			this.lvls_avIndex.push(0)				
			this.lvls_availables.push([])
			this.lvls_hasSingles.push(false)
			
			drawNodes(myDiagram)
	
			this.lvls_availables[this.lvl] = myDiagram.drawn.availables
			this.lvls_hasSingles[this.lvl] = myDiagram.drawn.singles.size > 0

			if (this.lvls_avIndex[this.lvl] < this.lvls_availables[this.lvl].length) {
				this.lvls_node.push(this.lvls_availables[this.lvl][this.lvls_avIndex[this.lvl]])
				this.lvls_node[this.lvl].marked = true
				this.lvls_node[this.lvl].markedColor = 'black'		
			} else {
				this.lvls_node.push(null)
			}
		},
		pop_lvl: function() {
			// [~] need to remove the current lvl seens			
			this.seen.removeAll(this.lvls_seen.pop())
			// and everything else on this lvl
			this.lvls_node.pop()
			this.lvls_hasSingles.pop()
			this.lvls_availables.pop()
			this.lvls_avIndex.pop()
			this.lvl -= 1			
			myDiagram.currentColor = hsl((15*this.lvl) % 360)			
		}
	}
			
	myDiagram.drawn = {
		looped_count: 0,
		availables: [],
		unreachable_cycle_count: 0,
		singles: new go.Set()
	}
			
	log("xk")
		
	myDiagram.nodes.each(node => {
	
		node.looped = false
		node.extended = false
		node.extendedColor = "red"
		node.nextNode = null
		node.prevNode = null
		node.nextLink = null
		node.prevLink = null
		node.shape = node.findObject("SHAPE")
		node.label = node.findObject("LABEL")
		node.shape.fill = "white"
		node.perm = myDiagram.perms[node.key]
		node.address = node.part.data.address			
		node.suivant = false
		node.dessus = false
		node.backed = false
		node.backedColorHue = 60
		node.marked = false

		// all normal nodes are available at start for extending as they're unblemished
		node.availabled = true
						
		// everyone is either a center or a normal node
		node.isCenter = node.part.data.isCenter
		
		// everyone knows its cycle index
		node.cycleIndex = node.part.data.cc
		
		// everyone holds a link to its cycle center
		node.cycleCenterNode = myDiagram.findNodeForKey("CC"+node.cycleIndex)
		
		// [1] each center node holds links to its N child nodes
		node.cycleChildNodes = new go.Set()
		
		
		// [2] each normal node holds links to its (N-2)*N potential nodes (nodes looped in when extended from this node)
		node.potentials = new go.Set()
		
		// [3] each normal node holds links to its (N-2) base nodes (nodes that when extended, loop in this node as well among others)
		node.bases = new go.Set();

	 	// [4] each normal node is CURRENTLY potentialed by up to (N-2) base nodes
		node.potentialedBy = new go.Set()	
		
		// [5] each node has a loop index (1-based as 0 means unparsed) for the loop it extends into
		node.loopIndex = 0
		
		// [6] each node has a loop color hue for the loop it extends into
		node.loopColorHue = 0
		
		// [8] this is user set and takes precedence over loopColorHue when drawing
		node.loopColor = null
		
		// [7] each node holds links to its N-2 brethren (nodes that extend into the same loop)
		node.loopBrethren = new go.Set()
		
		node.markedColor = 'black'
		
	})

	log("xk")
			
	myDiagram.links.each(link => {
		link.ctype = link.part.data.width / 2
		link.commited = false
		link.highlighted = false
		link.part.opacity = 0
		link.part.zOrder = 0
	})

	log("xk")
						
	var lix = 0 // current loop index
	var lch = 60 // current loop color hue
	var hueDelta = Math.max(1, Math.round(360 / (1 + myDiagram.nodes.filter(node=>!node.isCenter).count / (myDiagram.spClass - 1))))
	log("hueDelta" + hueDelta)
	myDiagram.nodes.each(node => {
	
		// for each normal node
		if (node.isCenter == false) {
			
			// [1] link this into its center node's child list
			// each node belongs to a single center
			node.cycleCenterNode.cycleChildNodes.add(node)

			// if this node has yet to be included in a loop
			if (node.loopIndex == 0) {
				// adapt current loop details to a new loop
				lix += 1
				lch = (lch + hueDelta) % 360
				
				// [5,6] this is the first node in the new loop
				node.loopIndex = lix
				node.loopColorHue = lch				
			}
						
			var next = node
			
			// for each cycle in the loop extension
			for (var j = 0; j < myDiagram.spClass - 2; j++) {
				// make the jump into the cycle
				next = myDiagram.findNodeForKey(myDiagram.pids[D2(myDiagram.perms[next.key])])
				
				// [2] potentials will be looped in if this node becomes availabled and then extended
				node.potentials.add(next)				
				
				// [3] bases will be unavailabled when this next node becomes looped in
				next.bases.add(node)
				
				// [4] all bases are available at start
				next.potentialedBy.add(node)
						
				for (var i = 0; i < myDiagram.spClass - 1; i++) {
					next = myDiagram.findNodeForKey(myDiagram.pids[D1(myDiagram.perms[next.key])])					 
					// [2] potential as well
					node.potentials.add(next)
				}
				
				// [7] the last node in the cycle is the one to make the jump, so we store it as a brethren of the current node
				node.loopBrethren.add(next)
				
				// [5,6] copy details from the first node in the current loop
				next.loopIndex = node.loopIndex
				next.loopColorHue = node.loopColorHue				
			}	
		}
	})
	
	postGenerate()
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

function drawNodes(diagram) {

	log("draw start")
									
	diagram.drawn.looped_count = 0	
	diagram.drawn.availables = []
	diagram.drawn.unreachable_cycle_count = 0
	diagram.drawn.singles.clear()
												
	diagram.nodes.each(node => {
	
		if(node.looped) {
			diagram.drawn.looped_count += 1
	
			if(node.availabled && !node.extended) {
				diagram.drawn.availables.push(node)
			}
		}
		
		if (node.isCenter) {
			var av = 0, lp = false, lf = null
			node.cycleChildNodes.each(leaf => {				
				if (leaf.looped) // if any node is looped, then the whole cycle is considered looped
						lp = true
				if (leaf.availabled) {
						av += 1
						lf = leaf // retain a leaf in case it's single
				}
			})
			node.label.text = node.cycleIndex + "\n[" + av + "]"
			node.shape.stroke = node.backed ? 'yellow' : (av == 0 && !lp ? 'red' : 'black')
			node.shape.strokeWidth = lp ? 1 : 24
			node.shape.strokeDashArray = (av == 0 ? null : [2, (300-2*(av-1))/(av)])
			if (!lp) {
				if (av == 0) {
					diagram.drawn.unreachable_cycle_count += 1
				} else if (av == 1 && lf.loopBrethren.filter(bro => bro.looped).count == 1) {
					diagram.drawn.singles.add(lf.loopBrethren.filter(bro => bro.looped).first())
				}
			}
		} else if (node.marked) {
			node.shape.stroke = node.markedColor
			node.shape.strokeWidth = 144
			node.shape.strokeDashArray = [6, 12]		
		} else if (node.backed) {
			node.shape.stroke = node.loopColor || hsl(node.loopColorHue)
			node.shape.strokeWidth = 144
			node.shape.strokeDashArray = [6, 12]
		} else if (node.suivant && !node.dessus) {
			node.shape.stroke = node.extended ? node.extendedColor : (node.loopColor || hsl(node.loopColorHue))
			node.shape.strokeWidth = 72
			node.shape.strokeDashArray = [12, 6]			
		} else if (node.extended) {
			node.shape.stroke = node.extendedColor
			node.shape.strokeWidth = 36
			node.shape.strokeDashArray = [12, 6]
		} else if (node.availabled) {
			node.shape.stroke = node.loopColor || hsl(node.loopColorHue)
			node.shape.strokeWidth = 24
			node.shape.strokeDashArray = [12, 6]
		} else {
			node.shape.stroke = 'black'
			node.shape.strokeWidth = 1
			node.shape.strokeDashArray = null
		}		
	})	

	log("draw before singles")
			
	diagram.drawn.singles.each(single => {
		var bro = single
		bro.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
		bro.shape.strokeWidth = 72
		bro.shape.strokeDashArray = [1, 1]
		bro.cycleCenterNode.shape.stroke = 'purple'
		bro.cycleCenterNode.shape.strokeWidth = 48
		bro.cycleCenterNode.shape.strokeDashArray = null
	
		single.loopBrethren.each(bro => {
			bro.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
			bro.shape.strokeWidth = 72
			bro.shape.strokeDashArray = [1, 1]
			bro.cycleCenterNode.shape.stroke = 'purple'
			bro.cycleCenterNode.shape.strokeWidth = 48
			bro.cycleCenterNode.shape.strokeDashArray = null
		})
	})
	
	log("draw before sort")
	diagram.drawn.availables.sort(function (a, b) {
		var p = diagram.drawn.singles.has(a) ? 1 : 0
		var q = diagram.drawn.singles.has(b) ? 1 : 0
		return q - p
	})
	
	log("draw after sort")
		
	var ss = diagram.ss
	var w = "{"+ss.state+"} ["+ss.lvl+"]"
		log("draw before walked loop")
	for(var i = 0; i <= ss.lvl; ++i)
		w += "&nbsp;" + (ss.lvls_avIndex[i]+1) + '/<b style="color:' + (ss.lvls_hasSingles[i] ? "red" : "black") + '">' + ss.lvls_availables[i].length + "</b>"
	document.getElementById("walked").innerHTML = w
	
	log("draw before status")
		
	var status = "looped: " + diagram.drawn.looped_count + " | availables: " + diagram.drawn.availables.length + " | unreachable: " + diagram.drawn.unreachable_cycle_count + " | singles: " + diagram.drawn.singles.size + " | is current single: " + diagram.drawn.singles.has(diagram.drawn.availables[0])
	document.getElementById("status").innerHTML = status	
	
	log("draw done.")
}

function resetDiagram(diagram) {
	var curr = diagram.startNode
	var next = null
	while(curr != null) {
		next = curr.nextNode
		removeAvailables(diagram, curr, next)
		if(next != null)
			deletePath(diagram, curr, next, true)
		
		curr = next
	}
	
	diagram.startNode = null
	
	diagram.nodes.each(node => {
		node.extended = node.availabled = false
		node.suivant = node.dessus = false		
		node.extendedColor = 'white'
		node.shape.fill = 'white'
		node.nextNode = null
		node.prevNode = null
		node.nextLink = null
		node.prevLink = null
		addAvailables(diagram, node, null)
	})
	
	// [~] and reset links
	
	drawNodes(diagram)
}

