#include "h.h"

/* data stack */
 CELL D[Dsz]; uint16_t Dp=0;	/* [D]ata [p]ointer */
/* return stack */
UCELL R[Rsz]; uint16_t Rp=0;	/* [R]eturn [p]ointer */

void VM() {}	/* virtual machine startup */

#ifdef EMULATOR
/* this code will be compiled only for emulator */
int main() { VM(); return 0; }
#endif
