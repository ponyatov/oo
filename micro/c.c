#include "h.h"

uint8_t M[Msz]; uint16_t Cp=0;								/* memory image */

void B(uint8_t  byte) { M[Cp++]=byte; }						/* compile byte */
void W(uint16_t word) { M[Cp++]=word; M[Cp++]=word>>8; }	/* 16 bit word  */

void set(uint16_t addr, uint16_t word) { M[addr+0]=word; M[addr+1]=word>>8; }
uint16_t get(uint16_t addr) { return M[addr+0]|(M[addr]<<8); }

void LFA() { W(get(LATEST)); }

void NFA(char* name) {
	uint8_t len = strlen(name);
	B(len); memcpy(&M[Cp],name,len); Cp += len;
}

void AFA(uint8_t attr) { B(attr); }

void CFA() { set(ENTRY,Cp); }

void SAVE(const char *bcfile) {
	FILE *img = NULL;
	assert(img = fopen(bcfile, "wb"));
	assert(fwrite(M, 1, Cp, img) == Cp);
	fclose(img);
}

void DUMP() {
	uint16_t addr; char buf[0x10]; uint8_t bufptr=0; buf[0]=0;
	for (addr = 0; addr < Cp; addr++) {
		if (addr % 0x10 == 0)
			printf("\t%s\n%.4X: ", buf,addr), buf[0]=0;
		printf("%.2X ", M[addr]);
		if (M[addr] >= 0x20) buf[bufptr++] = M[addr]; /* fill ASCII dump buffer */
		else buf[bufptr++] = '.';
		buf[bufptr]=0;
	}
	printf("\t%s\n\n",buf);
}
