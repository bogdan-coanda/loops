  function init() {
    var $ = go.GraphObject.make;  // for conciseness in defining templates

    myDiagram =
      $(go.Diagram, "myDiagramDiv", // must be the ID or reference to div
        {
          initialAutoScale: go.Diagram.Uniform,
          padding: 10,
          contentAlignment: go.Spot.Center,
          layout: $(go.Layout, { 
          	isInitial: false, 
          	isOngoing: false 
          }),
          maxSelectionCount: 1
        });

		function uncommit(node, diagram) {
			node.findLinksOutOf().each(function(link) { 
				if (link.commited) {
					link.commited = false
					updateArrowCount(link, diagram)
					if (diagram.mirror != null) {
						diagram.mirror.findLinksOutOf().each(function(link) {
							if (link.commited) {
								link.commited = false
								updateArrowCount(link, diagram)
								diagram.mirror = link.toNode
							}
						})
					}
					uncommit(link.toNode, diagram)
				}
			})
		}

		function updateArrowCount(link, diagram) {
			var arrowType = link.part.data.width / 2
			diagram.arrowCount[arrowType] += link.commited ? 1 : -1
			document.getElementById("D"+arrowType+"_count").value = diagram.arrowCount[arrowType]
		}

		function nodeClicked(e, node) {
			var diagram = node.diagram;
			if (node.diagram === null) return;
	
			// === circle nodes are special === //
			if (node.key.toString().startsWith("CC")) {
				node.circled = !node.circled
		
				if (node.circled) {
					node.findObject("SHAPE").fill = diagram.currentColor
				} else {
					node.findObject("SHAPE").fill = 'white'
				}
		
				return // !!!
			}
			
			// === continue only on linked nodes === //			
			if ((diagram.mirror !== null || diagram.current !== null) && node.findLinksInto().filter(link => link.highlighted).count == 0) {
				return
			}
	
			// --- remember current node --- //
			diagram.current = node
				
			// --- set mirror node if null --- //
			if (diagram.mirror === null && diagram.mirror_function != null) {
				diagram.mirror = diagram.findNodeForKey(diagram.pids[diagram.mirror_function(diagram.perms[node.key])])
			}

			// --- reset node highlights --- //	
			diagram.nodes.each(function(nn) { 
				nn.highlighted = false 
				nn.mirror_highlighted = false
			})

			// --- highlight follow-up nodes --- //		
			var perm = diagram.perms[node.key]
			for (var i = 0; i < diagram.spClass - 2; ++i) {
				perm = D2(perm)
				diagram.findNodeForKey(diagram.pids[perm]).highlighted = true
				for (var j = 0; j < diagram.spClass - 1; ++j) {
					perm = D1(perm)
					diagram.findNodeForKey(diagram.pids[perm]).highlighted = true
				}
			}
			perm = D2(perm)
			diagram.findNodeForKey(diagram.pids[perm]).highlighted = true

			// --- ?? --- //
			// node.findObject("LABEL").stroke = "white"

			// --- commit incoming links --- //
			// --- sets mirror node --- // 
			node.findLinksInto().each(function(link) { 
				if (link.highlighted && !link.commited) {
					link.commited = true;
					updateArrowCount(link, diagram)
					link.part.opacity = 1
					link.part.zOrder = 100
					if (diagram.mirror != null) {
						diagram.mirror.findLinksInto().each(function(mlink) {
							if (mlink.part.data.width == link.part.data.width) {
								mlink.commited = true
								updateArrowCount(link, diagram)
								mlink.part.opacity = 1
								mlink.part.zOrder = 100
								diagram.mirror = mlink.fromNode
							}
						})
					}
				}
			}); 
			
			// --- uncommit next links (if we backtraced) --- //
			// --- updates mirror node if needed --- //
			uncommit(node, diagram)
		
			// --- highlight follow-up mirror nodes --- //					
			if (diagram.mirror != null) {
				var perm = diagram.perms[diagram.mirror.key]
				for (var i = 0; i < diagram.spClass - 2; ++i) {
					perm = R2(perm)
					diagram.findNodeForKey(diagram.pids[perm]).mirror_highlighted = true
					for (var j = 0; j < diagram.spClass - 1; ++j) {
						perm = R1(perm)
						diagram.findNodeForKey(diagram.pids[perm]).mirror_highlighted = true
					}
				}
				perm = R2(perm)
				diagram.findNodeForKey(diagram.pids[perm]).mirror_highlighted = true
			}
			// --- reset all uncommited links --- //
			diagram.links.each(function(link) {
				if (!link.commited) {
					link.highlighted = false
					link.part.opacity = 0
					link.part.zOrder = 0
				}
			});

			// --- highlight potential next links --- //
			node.findLinksOutOf().each(function(link) { 
				link.highlighted = true
				link.part.opacity = 0.2
				link.part.zOrder = 50
			});
		
			// --- highlight potential next mirror links --- //		
			if (diagram.mirror != null) {
				diagram.mirror.findLinksInto().each(function(link) { 
					link.highlighted = true
					link.part.opacity = 0.2
					link.part.zOrder = 50
				});
			}
			
			// --- set current node colors --- //
			diagram.current.part.data.color = diagram.currentColor
			if (diagram.mirror != null) {
				diagram.mirror.part.data.color = diagram.currentColor
			}
				
			// --- color-in all 'normal' nodes --- // 
			diagram.nodes.filter(nn => nn.key.toString().startsWith("CC") == false).each(function(nn) {
				var color = (nn === diagram.current || nn === diagram.mirror) ? "red" : (nn.findLinksConnected().filter(link => link.commited).count == 0 ? "white" : nn.part.data.color)

				var shape = nn.findObject("SHAPE")
				shape.fill = color
				if(nn.highlighted) {
					shape.stroke = 'black'
					shape.strokeWidth = 24
					shape.strokeDashArray = [12, 6]
				} else if (nn.mirror_highlighted) {
					shape.stroke = 'gray'
					shape.strokeWidth = 24
					shape.strokeDashArray = [12, 6]
				} else {
					shape.stroke = 'black'
					shape.strokeWidth = 1
					shape.strokeDashArray = null
				}
			})
		}

    // define the Node template
    myDiagram.nodeTemplate =
      $(go.Node, "Spot", {
          locationSpot: go.Spot.Center,  // Node.location is the center of the Shape
          locationObjectName: "SHAPE",
          selectionAdorned: false,
          //selectionChanged: nodeSelectionChanged,
          click: nodeClicked
        },
        new go.Binding("location", "loc"),
        $(go.Panel, "Auto",
          $(go.Shape, "Ellipse", { 
          		name: "SHAPE",
              fill: "lightgray",  // default value, but also data-bound
              stroke: "black",  // modified by highlighting
              strokeWidth: 1,
              desiredSize: new go.Size(96, 96),
              portId: ""  // so links will go to the shape, not the whole node
            }
          )
        ),
        $(go.TextBlock, {
        		name: "LABEL",
        		font: "italic 700 16px sans-serif", 
        		stroke: "black" 
        	},
          new go.Binding("text")
        )
      );

    // define the Link template
    myDiagram.linkTemplate =
      $(go.Link, {
        	selectable: false,      // links cannot be selected by the user
        	curve: go.Link.Bezier,
        	layerName: "Background"  // don't cross in front of any nodes
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

    generateGraph();
    myDiagram.current = null;
    myDiagram.mirror = null;
    myDiagram.currentColor = "yellow"
    myDiagram.arrowCount = [0, 0, 0, 0, 0]
    myDiagram.mirror_function = null
  }
