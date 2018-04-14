  function postGenerate() {		
		
		set_as_looper()

		nodeClicked(null, myDiagram.findNodeForKey(myDiagram.pids[myDiagram.startPerm]))
				
		drawNodes(myDiagram)		
	}		  

function init() {

	myDiagram = $(go.Diagram, "myDiagramDiv", {
	
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
				
	myDiagram.forest = {
		state: "ground",
		initTime: 0,
		lvl: 0, 
		seen: new go.Set(), 
		lvls_node: [], 
		lvls_seen: [], 
		lvls_availables: [], 
		lvls_avIndex: [],
		lvls_hasSingles: [],
		lvls_hasUnreachables: [],
		trees: [],
		lvls_treeIndex: [],

		init: function() {
			this.state = "growing"
			this.initTime = new Date() 

			measureNodes(myDiagram)
			
			this.collectSeeds()
			
			this.lvl = -1
			this.push_lvl()
		},
		
		push_availables: function() {
			this.lvls_hasUnreachables.push(myDiagram.drawn.unreachable_cycle_count != 0)
			this.lvls_hasSingles.push(myDiagram.drawn.singles.size > 0)
			
			if(myDiagram.drawn.unreachable_cycle_count != 0) {
				this.lvls_availables.push([])
			} else if(myDiagram.drawn.singles.size > 0) {			
				this.lvls_availables.push([myDiagram.drawn.singles.first()])
			} else {
				this.lvls_availables.push(myDiagram.drawn.availables.filter(node => node.seedType == this.lvls_treeIndex[this.lvl]))
			}
						
			this.lvls_avIndex.push(-1)
			this.lvls_node.push(null)
		},
		
		next_available: function() {
			this.lvls_avIndex[this.lvl] = this.lvls_avIndex[this.lvl] + 1
			
			if (this.lvls_avIndex[this.lvl] < this.lvls_availables[this.lvl].length) {
				this.lvls_node[this.lvl] = this.lvls_availables[this.lvl][this.lvls_avIndex[this.lvl]]
			} else {
				this.lvls_node[this.lvl] = null
			}
		},

		push_lvl: function() {
		
			measureNodes(myDiagram)		
									
			this.lvl += 1
			this.lvls_seen.push(new go.Set())
			this.lvls_treeIndex.push(this.measureTrees())
			this.push_availables()		
			this.next_available()				
		},
		
		pop_lvl: function() {
			// [~] need to remove the current lvl seens
			this.seen.removeAll(this.lvls_seen.pop())
			// and everything else on this lvl
			this.lvls_treeIndex.pop()			
			this.lvls_hasUnreachables.pop()
			this.lvls_hasSingles.pop()
			this.lvls_availables.pop()
			this.lvls_avIndex.pop()			
			this.lvls_node.pop()
			this.lvl -= 1			
		},
						
		collectSeeds: function() {			
			this.trees = []
			
			var colorDiff = 360 / myDiagram.spClass
			for(var i = 0; i < myDiagram.spClass - 1; i++) {
				var color = hsl((60 + (i+1)*colorDiff) % 360, 33)
				
				var embryos = new go.List()
				embryos.addAll(myDiagram.nodes.filter(node => myDiagram.drawn.availables.includes(node) && node.seedType == i))
/*				embryos.each(node => {
					node.marked = true
					node.markedColor = color
				})*/
				
				this.trees.push({
					color: color,
					year: 0,
					years_embryos: [ embryos ],
				})
			}
		},
		
		measureTrees: function() {
			
			var mint = 0
			var lent = this.trees[0].years_embryos.length
			var year = this.trees[0].year
			for(var t = 1; t < this.trees.length; t++) {
				if(this.trees[t].year < year) {
					mint = t
					year = this.trees[t].year
					lent = this.trees[t].years_embryos.length				
				} else if(this.trees[t].year == year && this.trees[t].years_embryos.length < lent) {
					mint = t
					lent = this.trees[t].years_embryos.length
				}
			}
			
			return mint
		},
		
		grow: function(node) {
			var tree = this.trees[node.seedType]
			tree.year += 1
			
			node.potentials.each(n => n.seedType = node.seedType)
			var embryos = new go.List()
			embryos.addAll(node.potentials.filter(n => myDiagram.drawn.availables.includes(n)))
			tree.years_embryos.push(embryos)
		},
		
		trim: function(node) {
			this.trees[node.seedType].year -= 1
			this.trees[node.seedType].years_embryos.pop()
		}
						
	}
				
	postGenerate()
}

max_looped_count = 0

function measureNodes(diagram) {
	
	diagram.drawn.looped_count = 0	
	diagram.drawn.availables = []
	diagram.drawn.unreachable_cycle_count = 0
	diagram.drawn.singles.clear()
											
	var node = diagram.startNode
	while (node != null) {
		if(node.looped) {
			diagram.drawn.looped_count += 1	
			if(node.availabled && !node.extended) {
				diagram.drawn.availables.push(node)
			}
		}		
		node = node.nextNode
	}
														
	diagram.centers.each(node => {
		
		var av = 0, lp = false, lf = null
		node.cycleChildNodes.each(leaf => {				
			if (leaf.looped) // if any node is looped, then the whole cycle is considered looped
					lp = true
			if (leaf.availabled) {
					av += 1
					lf = leaf // retain a leaf in case it's single
			}
		})
		if (diagram.cursive) {
			node.label.text = node.cycleIndex + "\n[" + av + "]"
			node.shape.stroke = node.backed ? 'yellow' : (av == 0 && !lp ? 'red' : 'black')
			node.shape.strokeWidth = lp ? 1 : (av == 0 ? 240 : 24)
			node.shape.strokeDashArray = (av == 0 ? [2, 2] : [2, (300-2*(av-1))/(av)])
		}
		if (!lp) {
			if (av == 0) {
				diagram.drawn.unreachable_cycle_count += 1
			} else if (av == 1 && lf.loopBrethren.filter(bro => bro.looped).count == 1) {
				diagram.drawn.singles.add(lf.loopBrethren.filter(bro => bro.looped).first())
			}
		}
	})
	
	if (diagram.drawn.looped_count > max_looped_count)
		max_looped_count = diagram.drawn.looped_count
}

function drawNodes(diagram) {

	diagram.nodes.each(node => {
			
		if (node.isCenter) {
			// bla bla
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
			
	diagram.drawn.singles.each(single => {
		var bro = single
		bro.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
		bro.shape.strokeWidth = 72
		bro.shape.strokeDashArray = [1, 1]
		bro.cycleCenterNode.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
		bro.cycleCenterNode.shape.strokeWidth = 48
		bro.cycleCenterNode.shape.strokeDashArray = null
	
		single.loopBrethren.each(bro => {
			bro.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
			bro.shape.strokeWidth = 72
			bro.shape.strokeDashArray = [1, 1]
			bro.cycleCenterNode.shape.stroke = bro.loopColor || hsl(bro.loopColorHue)
			bro.cycleCenterNode.shape.strokeWidth = 48
			bro.cycleCenterNode.shape.strokeDashArray = null
		})
	})
	
	if(diagram.cursive == false) {	
		diagram.links.each(link => {
			if(link.commited) {
				link.part.opacity = 1
				link.part.zOrder = 100
			} else {
				link.part.opacity = 0
				link.part.zOrder = 0
			}
		})
	}
	
	if (diagram.forest.state != "ground") {
		diagram.forest.lvls_availables[diagram.forest.lvl].forEach(node => {
			node.shape.stroke = (node == diagram.forest.lvls_node[diagram.forest.lvl] ? 'black' : diagram.forest.trees[node.seedType].color)
			node.shape.strokeWidth = 72
			node.shape.strokeDashArray = [12, 6]			
		})
	}
	
	solution(diagram)
	updateStatus(diagram)
}

function updateStatus(diagram) {

	if (diagram.forest.state != "ground") {
			
		var w = "{ "+diagram.forest.state+" » ee:"+diagram.eecc+" @ " + tstr(new Date() - diagram.forest.initTime) + " } ["+diagram.forest.lvl+"]"
		for(var i = 0; i <= diagram.forest.lvl; ++i) {
			var color = diagram.forest.lvls_node[i] == null ? 'gray' : diagram.forest.trees[diagram.forest.lvls_node[i].seedType].color
			w += '&nbsp;<b style="color:' + color + '">'
			w += (diagram.forest.lvls_avIndex[i]+1) 
			w += '/<b style="color:' + (diagram.forest.lvls_hasUnreachables[i] ? "gray" : (diagram.forest.lvls_hasSingles[i] ? "black" : color)) + '">' + diagram.forest.lvls_availables[i].length + "</b></b>"
		}
		document.getElementById("walked").innerHTML = w	
			
		var status = "max: " + max_looped_count + " | looped: " + diagram.drawn.looped_count + " | availables: " + diagram.drawn.availables.length + " | unreachable: " + diagram.drawn.unreachable_cycle_count + " | singles: " + diagram.drawn.singles.size + " | is current single: " + diagram.drawn.singles.has(diagram.drawn.availables[0])
		document.getElementById("status").innerHTML = status	
		
		if(diagram.cursive)
			solution(diagram)
			
	} else {

		var ss = diagram.ss
		var w = "{ "+ss.state+" » jk:"+diagram.jkcc+" @ " + tstr(new Date() - ss.initTime) + " } ["+ss.lvl+"]"
		for(var i = 0; i <= ss.lvl; ++i)
			w += "&nbsp;" + (ss.lvls_avIndex[i]+1) + '/<b style="color:' + (ss.lvls_hasSingles[i] ? "red" : "black") + '">' + ss.lvls_availables[i].length + "</b>"
		document.getElementById("walked").innerHTML = w	
			
		var status = "max: " + max_looped_count + " | looped: " + diagram.drawn.looped_count + " | availables: " + diagram.drawn.availables.length + " | unreachable: " + diagram.drawn.unreachable_cycle_count + " | singles: " + diagram.drawn.singles.size + " | is current single: " + diagram.drawn.singles.has(diagram.drawn.availables[0])
		document.getElementById("status").innerHTML = status	
		
		if(diagram.cursive)
			solution(diagram)
	}
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

function solution(diagram) {
	var node = diagram.startNode
	if (node == null)
		return
		
	var next = node.nextNode
	var sol = node.perm
	while (next != null) {
		sol += next.perm.substr(-node.nextLink.ctype)
		node = next
		next = node.nextNode
	}
	
	diagram.solution = sol
	document.getElementById("solution").innerHTML = diagram.ss.state == "done." ? '<b style="color:' + (sol == "01234501324501342501345201354201352401352041352014352013450213405214305214035214053214503214530214532014532104523104521304521034521043521045321405231402531402351402315402314502314052134025134021534021354021345012340512340152340125340123540123045123041523041253041235041230541230145230142530142350142305142301542301245301243502143502413502431502435102453102451302451032451023415023410524310524130524103524105324150324153024153204153240153241052341025341023541023451024350124305124301524301254302154320154321054231054213054210354210534201534205132405132045132054132051432051342053142035142031542031452031425031420534120354120345120341520341250341205342105432150423150421350421530421503421504325104235104253104251304251034251043250143250413250431205431204531204351204315204312504321540325140325410325401325403124503124053124035124031524031254032154302514302541302543102543012" ? (diagram.jkcc == 543163 ? "blue" : 'orange') : "red") + '">'+sol+'</b>' : sol
}
