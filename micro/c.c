#include "h.h"

BYTE M[Msz]; UCELL Cp=0; 									/* memory image */

void B( BYTE byte) { M[Cp++]=byte; }						/* compile byte */
void W(UCELL word) { M[Cp++]=word; M[Cp++]=word>>8; }		/* 16 bit word  */

void set(UCELL addr, UCELL word) { M[addr+0]=word; M[addr+1]=word>>8; }
UCELL get(UCELL addr) { return M[addr+0]|(M[addr+1]<<8); }

void LFA() { W(get(LATEST)); }

void NFA(char* name) {
	BYTE len = strlen(name);
	int i; for (i=0;i<len;i++) name[i]=toupper(name[i]);
	B(len); memcpy(&M[Cp],name,len); Cp += len;
}

void AFA(BYTE attr) { B(attr); }

void CFA() { set(ENTRY,Cp); }

void SAVE(const char *bcfile) {
	FILE *img = NULL;
	assert(img = fopen(bcfile, "wb"));
	assert(fwrite(M, 1, Cp, img) == Cp);
	fclose(img);
}

void LOAD(const char *bcfile) {
	FILE *img = NULL;
	assert(img = fopen(bcfile, "rb"));
	Cp = fread(M, 1, Msz, img); assert(Cp>0); assert(Cp<Msz);
	fclose(img);
}

void DUMP() {
	UCELL addr; char buf[0x10]; uint8_t bufptr=0; buf[0]=0;
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
