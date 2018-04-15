function init() {

	myDiagram = $(go.Diagram, "myDiagramDiv", {
	
	myDiagram.ss = {
		
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

