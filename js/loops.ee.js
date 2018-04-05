function ee(diagram) {

	log(diagram.forest.state)

	if (diagram.forest.state == "done.")
		return

	diagram.eecc += 1	
	
	if (diagram.forest.state == "ground") {
		
		diagram.forest.init()
		
	} else if (diagram.forest.state == "growing") {
	
		if (diagram.drawn.looped_count == diagram.perms.length) {
		
			diagram.forest.state = "done."
			log("FOUND!!!")
			
		} else if (diagram.forest.lvls_node[diagram.forest.lvl] == null) {
			
			// just another dead end ⇒ backtrack one lvl
			diagram.forest.pop_lvl()	
			
			if (diagram.forest.lvl == -1) { // sanity

				diagram.forest.state = "done."				
				log("NOT FOUND?!?")

			}	else {
		
				// and clean up previous lvl trial
				collapseFast(diagram, diagram.forest.lvls_node[diagram.forest.lvl])
				diagram.forest.seen.add(diagram.forest.lvls_node[diagram.forest.lvl])
				diagram.forest.lvls_seen[diagram.forest.lvl].add(diagram.forest.lvls_node[diagram.forest.lvl])
						
				// and continue
				diagram.forest.next_available()
			}
			
		} else { // normal, extendable node
		
			if (diagram.forest.seen.has(diagram.forest.lvls_node[diagram.forest.lvl]) == false && extendFast(diagram, diagram.forest.lvls_node[diagram.forest.lvl])) {		
			
				diagram.forest.push_lvl()
				
			} else {

				// or continue
				diagram.forest.next_available()
					
			}			
		}
	}
	
	measureNodes(diagram)
	drawNodes(diagram)
}

