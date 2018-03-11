#include "h.h"

uint8_t M[Msz]; uint16_t Mp=0;								/* memory image */

void B(uint8_t  byte) { M[Mp++]=byte; }						/* compile byte */
void W(uint16_t word) { M[Mp++]=word; M[Mp++]=word>>8; }	/* 16 bit word  */

void LFA(UCELL prev) { W(prev); }

void SAVE(const char *bcfile) {
	FILE *img=NULL;
	assert( img=fopen(bcfile,"wb") );
	assert( fwrite(M,1,Mp,img)==Mp );
	fclose(img);
}
