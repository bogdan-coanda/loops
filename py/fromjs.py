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
	myDiagram.k3cc = -2
	myDiagram.k2cc = -1
	myDiagram.k1cc = -1
	
	myDiagram.startPerm = generateGraph();
	log("xk")
	myDiagram.startNode = null;
	myDiagram.solution = ""
	myDiagram.mode = "LOOP"
	myDiagram.currentColor = "yellow"
	myDiagram.currentColorHue = 60
	myDiagram.arrowCount = [0, 0, 0]
	myDiagram.available_count	
		
	myDiagram.jkcc = 0	
	myDiagram.RR = 120000
	myDiagram.mxlvl = 0
	myDiagram.auto = true
	myDiagram.cursive = false // [~]
	myDiagram.ss = {
		state: "new",
		initTime: 0,
		lvl: 0, 
		seen: new go.Set(), 
		lvls_node: [null], 
		lvls_seen: [new go.Set()], 
		lvls_availables: [[]], 
		lvls_avIndex: [0],
		lvls_hasSingles: [false],
		
		init: function() {
			this.state = "running"
			this.initTime = new Date() 
			measureNodes(myDiagram)
		
			myDiagram.drawn.availables.sort(function (a, b) {
				var p = myDiagram.drawn.singles.has(a) ? 1 : 0
				var q = myDiagram.drawn.singles.has(b) ? 1 : 0		
				return p != q ? q - p : b.pid - a.pid
			})				
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
			
			measureNodes(myDiagram)

			myDiagram.drawn.availables.sort(function (a, b) {
				var p = myDiagram.drawn.singles.has(a) ? 1 : 0
				var q = myDiagram.drawn.singles.has(b) ? 1 : 0
				return p != q ? q - p : b.pid - a.pid			
			})	
						
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
			if (this.lvls_node[this.lvl] != null) {
				this.lvls_node[this.lvl].marked = false
			}				
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
		node.pid = node.part.data.pid
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
	
	myDiagram.centers = myDiagram.nodes.filter(node => node.isCenter)
		
	postGenerate()
}
