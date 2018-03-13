var M  = new Uint8Array(Msz);				// main memory
var Ip = 0;									// instuction point
var Cp = 0;									// compiler (heap) pointer

// bytecode loader

document.getElementById('bytecode').addEventListener('change', function (event) {
	  const files = event.target.files;
	  const reader = new FileReader();
	  
	  reader.onload = function(e) {
		  M = new Uint8Array(e.target.result);
		  console.log(M);
		  VM();								// run system
		}
	  Cp = files[0].size;
	  if ( Cp > Msz) alert(">Msz");
	  else reader.readAsArrayBuffer(files[0]);

	}, false);
