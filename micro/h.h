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
#include <ctype.h>
#include <string.h>
#include <assert.h>
#endif

/* set 16/32 bit mode
	CELL is machine word for FORTH systems */
#define  BYTE  uint8_t
#define  CELL  int16_t	/* light microcontrollers */
#define UCELL uint16_t

extern BYTE M[]; extern UCELL Cp; extern UCELL Ip;			/* memory image */
extern void B(BYTE  byte);									/* compile byte */
extern void W(UCELL word);									/* compile 16bit */

extern void set(UCELL addr, UCELL word);					/* set 16bit */
extern UCELL get(UCELL addr);							/* get 16bit */

#define ENTRY  0x0001	/* jmp _entry */
#define HEAP   0x0003	/* Cp to first free byte */
#define LATEST 0x0005	/* LATEST defined word */

extern void LFA();									/* compile LFA */
extern void NFA(char* name);						/* compile NFA */
extern void AFA(BYTE attr);
extern void CFA();									/* patch entry point */

extern void SAVE(const char *bcfile);				/* save memory image */
extern void LOAD(const char *bcfile);
extern void DUMP();									/* dump memory image */

/* command opcodes constants */

#define NOP		0x00
#define BYE		0xFF
													/* control flow */
#define JMP		0x01
#define qJMP	0x02
#define CALL	0x03
#define RET		0x04
													/* debug */
#define LABEL	0xD0

#endif /* _H_uFORTH */
