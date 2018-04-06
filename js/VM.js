D = [ ]		// data stack
R = [ ]		// return stack
W = { }		// vocabulary

W.nop = function nop() {}	// empty VM command
W.bye = function bye() {}	// stop system

W.words = function words() {
	log.innerHTML += '\n';
	for (i in W) log.innerHTML += i+'\t';
	log.innerHTML += '\n';
}

var log;
var pad;
var net;	// network status
var logo;

window.onload = function entry () { // system init entry point
	log  = document.getElementById('log'); 
	pad  = document.getElementById('pad');
	logo = document.getElementById('logo');
	W.words();
	console.log(W.nop);
	log.onclick = W.interpret;
}

var PAD = '';				// here input script will be stored

W.word = function word() {
	var SRC = pad.value ; console.log(SRC);			// input
	var STATE = {		// finit automata states
			TRAIL:0,	// trailing spaces
			COMMENT:1,	// in comment
			DATA:2		// parsing output data
	};
	console.log(SRC);
}
//	log.innerHTML += '\n' + pad.value + '\n'; }

W.interpret = function interpret() {	// interpreter run on log click 
	PAD = pad.value;					// copy script from input field
	while (PAD != '')
		log.innerHTML += WORD();
}

window.ononline = function () {
	document.body.style.backgroundColor ='black'; }
window.onoffline = function () {
	document.body.style.backgroundColor ='#440000'; }

