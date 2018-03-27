function log(txt) {
//	console.log(txt)
//	document.getElementById("log").innerHTML += "<br />" + txt
}

function nstr(node) {
	if (node == null)
		return "[null]"
	return "[" + node.key + "|" + node.perm + "|" + node.address + "]"
}

/*function hsl(hue) {
	return 'hsl(' + hue + ', 100%, 50%)'
}*/

function hsl(hue, light = 50) {
	return 'hsl(' + hue + ', 100%, ' + light + '%)'
}

