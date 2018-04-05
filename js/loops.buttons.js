function setCurrentColor() {
	var radios = document.getElementsByName("color_radio")
	for (var i = 0; i < radios.length; i++) 
		if (radios[i].checked) {
			myDiagram.currentColor = radios[i].parentNode.style["background-color"]
			myDiagram.currentColorHue = radios[i].value
			return
		}
}

function EA() {
	extendForMaxAvailability(myDiagram)
}

function EP() {
	extendForMaxPotentiality(myDiagram)
}

function EAPR() {
	extendForMinAPRatio(myDiagram)
}

function CLEAR() {
	document.getElementById("log").innerHTML = ""
}

function reset_diagram() {
	resetDiagram(myDiagram)
}

function QQ() {
	jk(myDiagram)
}

function EE() {
	ee(myDiagram)
}

function AutoSwitch() {
	myDiagram.auto = !myDiagram.auto
	if(myDiagram.auto) {
		document.getElementById("auto-button").style["background-color"] = 'red'
		document.getElementById("auto-button").innerHTML = 'AUTO'
	} else {
		document.getElementById("auto-button").style["background-color"] = 'green'
		document.getElementById("auto-button").innerHTML = 'MANUAL'
	}
}

function set_as_looper() {
	myDiagram.mode = "LOOP"
	document.getElementById("loop_button").style["background-color"] = 'darkorchid'
	document.getElementById("loop_button").style["color"] = 'white'
	document.getElementById("path_button").style["background-color"] = 'plum'
	document.getElementById("path_button").style["color"] = 'black'
	document.getElementById("mark_button").style["background-color"] = 'plum'
	document.getElementById("mark_button").style["color"] = 'black'
	document.getElementById("back_button").style["background-color"] = 'plum'
	document.getElementById("back_button").style["color"] = 'black'
	drawNodes(myDiagram)
}

function set_as_pather() {
	myDiagram.mode = "PATH"
	document.getElementById("loop_button").style["background-color"] = 'plum'
	document.getElementById("loop_button").style["color"] = 'black'
	document.getElementById("path_button").style["background-color"] = 'darkorchid'
	document.getElementById("path_button").style["color"] = 'white'
	document.getElementById("mark_button").style["background-color"] = 'plum'
	document.getElementById("mark_button").style["color"] = 'black'
	document.getElementById("back_button").style["background-color"] = 'plum'
	document.getElementById("back_button").style["color"] = 'black'
	drawNodes(myDiagram)
}

function set_as_marker() {
	myDiagram.mode = "MARK"
	document.getElementById("loop_button").style["background-color"] = 'plum'
	document.getElementById("loop_button").style["color"] = 'black'
	document.getElementById("path_button").style["background-color"] = 'plum'
	document.getElementById("path_button").style["color"] = 'black'
	document.getElementById("mark_button").style["background-color"] = 'darkorchid'
	document.getElementById("mark_button").style["color"] = 'white'
	document.getElementById("back_button").style["background-color"] = 'plum'
	document.getElementById("back_button").style["color"] = 'black'
	drawNodes(myDiagram)
}

function set_as_backer() {
	myDiagram.mode = "BACK"
	document.getElementById("loop_button").style["background-color"] = 'plum'
	document.getElementById("loop_button").style["color"] = 'black'
	document.getElementById("path_button").style["background-color"] = 'plum'
	document.getElementById("path_button").style["color"] = 'black'
	document.getElementById("mark_button").style["background-color"] = 'plum'
	document.getElementById("mark_button").style["color"] = 'black'
	document.getElementById("back_button").style["background-color"] = 'darkorchid'
	document.getElementById("back_button").style["color"] = 'white'
	drawNodes(myDiagram)
}

