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
#include <string.h>
#include <assert.h>
#endif

/* set 16/32 bit mode
	CELL is machine word for FORTH systems */
#define  CELL  int16_t	/* light microcontrollers */
#define UCELL uint16_t

extern uint8_t M[]; extern uint16_t Cp;						/* memory image */
extern void B(uint8_t  byte);								/* compile byte */
extern void W(uint16_t word);								/* compile 16bit */

extern void set(uint16_t addr, uint16_t word);				/* set 16bit */
extern uint16_t get(uint16_t addr);							/* get 16bit */

#define ENTRY  0x0001	/* jmp _entry */
#define HEAP   0x0003	/* Cp to first free byte */
#define LATEST 0x0005	/* LATEST defined word */

extern void LFA();									/* compile LFA */
extern void NFA(char* name);						/* compile NFA */
extern void AFA(uint8_t attr);
extern void CFA();									/* patch entry point */

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
