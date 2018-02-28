/* sizes of statically allocated structures */
#define Dsz 0x10
#define Rsz 0x100
#define Msz 0x1000

#include <stdint.h>					/* std.includes */
#ifdef EMULATOR						/* for emulator mode only */
#include <stdlib.h>
#endif

/* set 16/32 bit mode
	CELL is machine word for FORTH systems */
#define  CELL  int16_t	/* light microcontrollers */
#define UCELL uint16_t

/* data stack */
 CELL D[Dsz]; uint16_t Dp=0;	/* [D]ata [p]ointer */
/* return stack */
UCELL R[Rsz]; uint16_t Rp=0;	/* [R]eturn [p]ointer */

void VM() {}	/* virtual machine startup */

#ifdef EMULATOR
/* this code will be compiled only for emulator */
int main() { VM(); return 0; }
#endif
