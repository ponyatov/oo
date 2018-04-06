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

var PAD = '';			// here input script will be stored

W.word = function word() {
	WN = ''				// value will be returned
	var STATE = {		// DFA automata states
			TRAIL:0,		// trailing spaces
			LCOMMENT:1,		// # line \ comment
			BCOMMANE:11,	// ( block comment )
			DATA:2,			// collect non-space chars
			DONE:3,			// parsing done
	}; var S = STATE.TRAIL;	// [S]tate
	
	function getch() {
		var C = PAD[0] ; PAD = PAD.slice(1);
	return C; }
	
	function space(C) {
		if (C==' '|C=='\t'|C=='\n') return true;
		else return false;
	}
	
	while (S != STATE.DONE & PAD != '') {
		console.log('state',S);
		switch (S) {
		case STATE.TRAIL:
			var C = getch(); console.log('char',C);
			if (space(C)) break; // ignore
			if (C=='#'|C=='\\') { S=STATE.LCOMMENT; break; }
			if (C=='(') { S=STATE.BCOMMENT; break; }
			WN +=C; S = STATE.DATA; break;
		case STATE.LCOMMENT:
			if (getch()=='\n') S = STATE.TRAIL; break;
		case STATE.DATA:
			var C = getch(); console.log('char',C);
			if (C==' '|C=='\t'|C=='\n') S=STATE.DONE; break;
			else WN += C; break;
		default: abort();
		}
	}
	PAD=''
	return WN
}
//	log.innerHTML += '\n' + pad.value + '\n'; }

W.interpret = function interpret() {	// interpreter run on log click 
	PAD = pad.value;					// copy script from input field
	while (PAD != '')
		log.innerHTML += W.word();
}

window.ononline = function () {
	document.body.style.backgroundColor ='black'; }
window.onoffline = function () {
	document.body.style.backgroundColor ='#440000'; }

