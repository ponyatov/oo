#include "h.h"

uint8_t M[Msz]; uint16_t Mp=0;								/* memory image */

void B(uint8_t  byte) { M[Mp++]=byte; }						/* compile byte */
void W(uint16_t word) { M[Mp++]=word; M[Mp++]=word>>8; }	/* 16 bit word  */

void LFA(UCELL prev) { W(prev); }

void SAVE(const char *bcfile) {
	FILE *img = NULL;
	assert(img = fopen(bcfile, "wb"));
	assert(fwrite(M, 1, Mp, img) == Mp);
	fclose(img);
}

void DUMP() {
	uint16_t addr; char buf[0x10]; uint8_t bufptr=0;
	for (addr = 0; addr < Mp; addr++) {
		if (addr % 0x10 == 0)
			printf("\n%.4X: ", addr);
		printf("%.2X ", M[addr]);
		buf[bufptr++] = M[addr];		/* fill ASCII dump buffer */
	}
	printf("\n");
}
