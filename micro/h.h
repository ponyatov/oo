#ifndef _H_uFORTH
#define _H_uFORTH

/* sizes of statically allocated structures */
#define Dsz 0x10
#define Rsz 0x100

#ifndef Msz
#define Msz 0x1000
#endif

#include <stdint.h>					/* std.includes */
#ifdef EMULATOR						/* for emulator mode only */
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#endif

/* set 16/32 bit mode
	CELL is machine word for FORTH systems */
#define  CELL  int16_t	/* light microcontrollers */
#define UCELL uint16_t

extern uint8_t M[]; extern uint16_t Mp;						/* memory image */
extern void B(uint8_t byte);								/* compile byte */

extern void LFA(UCELL prev);						/* compile LFA */

extern void SAVE(const char *bcfile);				/* save memory image */
extern void DUMP();									/* dump memory image */

/* command opcodes constants */

#define NOP		0x00
#define BYE		0xFF
#define JMP		0x01
#define qJMP	0x02
#define CALL	0x03
#define RET		0x04

#endif /* _H_uFORTH */
