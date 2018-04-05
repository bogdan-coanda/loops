function log(txt) {
	console.log(txt)
	document.getElementById("log").innerHTML += "<br />" + txt
}

function nstr(node) {
	if (node == null)
		return "[null]"
	return "[" + node.key + "|" + node.perm + "|" + node.address + "]"
}

function tstr(ms) {
	return "" + Math.floor(ms / 1000 / 60) + "m" + Math.floor((ms % (1000*60)) / 1000) + "s." + (ms % 1000)
}

/*function hsl(hue) {
	return 'hsl(' + hue + ', 100%, 50%)'
}*/

function hsl(hue, light = 50) {
	return 'hsl(' + hue + ', 100%, ' + light + '%)'
}

function divide(x, y) {
	return (x - (x % y)) / y
}
