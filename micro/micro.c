#include "h.h"

/* data stack */
 CELL D[Dsz]; uint16_t Dp=0;	/* [D]ata [p]ointer */
/* return stack */
UCELL R[Rsz]; uint16_t Rp=0;	/* [R]eturn [p]ointer */

UCELL Ip=0;

								/* virtual machine commands */

void _NOP() { printf("nop"); }
void _BYE() { printf("bye\n\n"); exit(0); }
void _JMP() { Ip = get(Ip); printf("jmp\t%.4X",Ip); assert(Ip<Cp); }

void VM() {						/* virtual machine startup */
	for (;;) {
		BYTE op = M[Ip++];
		printf("\n%.4X:%.2X\t",Ip-1,op);
		switch (op) {
			case NOP: _NOP(); break;
			case BYE: _BYE(); break;
			case JMP: _JMP(); break;
			default: abort();
		}
	}
}

#ifdef EMULATOR
/* this code will be compiled only for emulator */
int main(int argc, char* argv[]) {
	assert(argc==2); LOAD(argv[1]);
	VM(); return 0;
}
#endif
