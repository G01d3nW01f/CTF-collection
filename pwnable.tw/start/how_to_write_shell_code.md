


step1 write source code in C 
execve.c

```
#include <stdlib.h>

int main(){
	
	char *argv[] = {"/bin/sh", NULL};
	execve(argv[0], argv, NULL);
}
```

compile:

```
gcc -m32 -static execve.c

```

compiled: a.out

```
objdump -M intel -d a.out | sed -n '/<main>:/,/^$/p'
```
```
->$ objdump -M intel -d a.out | sed -n '/<main>:/,/^$/p'
080496d5 <main>:
 80496d5:	8d 4c 24 04          	lea    ecx,[esp+0x4]
 80496d9:	83 e4 f0             	and    esp,0xfffffff0
 80496dc:	ff 71 fc             	push   DWORD PTR [ecx-0x4]
 80496df:	55                   	push   ebp
 80496e0:	89 e5                	mov    ebp,esp
 80496e2:	53                   	push   ebx
 80496e3:	51                   	push   ecx
 80496e4:	83 ec 10             	sub    esp,0x10
 80496e7:	e8 3b 00 00 00       	call   8049727 <__x86.get_pc_thunk.ax>
 80496ec:	05 08 19 0a 00       	add    eax,0xa1908
 80496f1:	8d 90 14 b0 fc ff    	lea    edx,[eax-0x34fec]
 80496f7:	89 55 f0             	mov    DWORD PTR [ebp-0x10],edx
 80496fa:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [ebp-0xc],0x0
 8049701:	8b 55 f0             	mov    edx,DWORD PTR [ebp-0x10]
 8049704:	83 ec 04             	sub    esp,0x4
 8049707:	6a 00                	push   0x0
 8049709:	8d 4d f0             	lea    ecx,[ebp-0x10]
 804970c:	51                   	push   ecx
 804970d:	52                   	push   edx
 804970e:	89 c3                	mov    ebx,eax
 8049710:	e8 3b 29 02 00       	call   806c050 <__execve>
 8049715:	83 c4 10             	add    esp,0x10
 8049718:	b8 00 00 00 00       	mov    eax,0x0
 804971d:	8d 65 f8             	lea    esp,[ebp-0x8]
 8049720:	59                   	pop    ecx
 8049721:	5b                   	pop    ebx
 8049722:	5d                   	pop    ebp
 8049723:	8d 61 fc             	lea    esp,[ecx-0x4]
 8049726:	c3                   	ret
```


```
objdump -M intel -d a.out | sed -n '/__execve>:/,/^$/p'
```

```
->$ objdump -M intel -d a.out | sed -n '/__execve>:/,/^$/p'
0806c050 <__execve>:
 806c050:	53                   	push   ebx
 806c051:	8b 54 24 10          	mov    edx,DWORD PTR [esp+0x10]
 806c055:	8b 4c 24 0c          	mov    ecx,DWORD PTR [esp+0xc]
 806c059:	8b 5c 24 08          	mov    ebx,DWORD PTR [esp+0x8]
 806c05d:	b8 0b 00 00 00       	mov    eax,0xb
 806c062:	65 ff 15 10 00 00 00 	call   DWORD PTR gs:0x10
 806c069:	5b                   	pop    ebx
 806c06a:	3d 01 f0 ff ff       	cmp    eax,0xfffff001
 806c06f:	0f 83 ab 69 00 00    	jae    8072a20 <__syscall_error>
 806c075:	c3                   	ret
 806c076:	66 90                	xchg   ax,ax
 806c078:	66 90                	xchg   ax,ax
 806c07a:	66 90                	xchg   ax,ax
 806c07c:	66 90                	xchg   ax,ax
 806c07e:	66 90                	xchg   ax,ax
```

reversing in gdb
```
->$ gdb -q ./a.out
Reading symbols from ./a.out...
(No debugging symbols found in ./a.out)
(gdb) set-disassembly intel
Undefined command: "set-disassembly".  Try "help".
(gdb) disas execve
Dump of assembler code for function execve:
   0x0806c050 <+0>:	push   %ebx
   0x0806c051 <+1>:	mov    0x10(%esp),%edx
   0x0806c055 <+5>:	mov    0xc(%esp),%ecx
   0x0806c059 <+9>:	mov    0x8(%esp),%ebx
   0x0806c05d <+13>:	mov    $0xb,%eax
   0x0806c062 <+18>:	call   *%gs:0x10
   0x0806c069 <+25>:	pop    %ebx
   0x0806c06a <+26>:	cmp    $0xfffff001,%eax
   0x0806c06f <+31>:	jae    0x8072a20 <__syscall_error>
   0x0806c075 <+37>:	ret    
```

```
(gdb) b *0x0806c062
Breakpoint 2 at 0x806c062
(gdb) run
Starting program: /home/xxxxxx/xxx/xxxxxxxx/shellcode/a.out 

Breakpoint 2, 0x0806c062 in execve ()
(gdb) x/i $pc
=> 0x806c062 <execve+18>:	call   *%gs:0x10
(gdb) info register
eax            0xb                 11
ecx            0xffffcde8          -12824
edx            0x0                 0
ebx            0x80b6008           134963208
esp            0xffffcdc8          0xffffcdc8
ebp            0xffffcdf8          0xffffcdf8
esi            0x80eaff4           135180276
edi            0x1                 1
eip            0x806c062           0x806c062 <execve+18>
eflags         0x292               [ AF SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) info registers
eax            0xb                 11
ecx            0xffffcde8          -12824
edx            0x0                 0
ebx            0x80b6008           134963208
esp            0xffffcdc8          0xffffcdc8
ebp            0xffffcdf8          0xffffcdf8
esi            0x80eaff4           135180276
edi            0x1                 1
eip            0x806c062           0x806c062 <execve+18>
eflags         0x292               [ AF SF IF ]
cs             0x23                35
ss             0x2b                43
ds             0x2b                43
es             0x2b                43
fs             0x0                 0
gs             0x63                99
(gdb) x/4wx $ebx
0x80b6008:	0x6e69622f	0x0068732f	0x00000000	0x00000000
(gdb) x/s $ebx
0x80b6008:	"/bin/sh"
```


write assembly code

execve.s

```
        /* execve.s */
        .intel_syntax noprefix
        .globl _start
_start:
        push 0x0068732f
        push 0x6e69622f
        mov ebx, esp
        xor edx, edx
        push edx
        push ebx
        mov ecx, esp
        mov eax, 11
        int 0x80
```

compile:
```
gcc -nostdlib -m32 execve.s
```
object dump:

```
->$ objdump -M intel -d a.out

a.out:     file format elf32-i386


Disassembly of section .text:

00001000 <_start>:
    1000:	68 2f 73 68 00       	push   0x68732f
    1005:	68 2f 62 69 6e       	push   0x6e69622f
    100a:	89 e3                	mov    ebx,esp
    100c:	31 d2                	xor    edx,edx
    100e:	52                   	push   edx
    100f:	53                   	push   ebx
    1010:	89 e1                	mov    ecx,esp
    1012:	b8 0b 00 00 00       	mov    eax,0xb
    1017:	cd 80                	int    0x80
```
parse to "\x"

```
->$ objdump -M intel -d a.out | grep '^ ' | cut -f2 | perl -pe 's/(\w{2})\s+/\\x\1/g'
\x68\x2f\x73\x68\x00\x68\x2f\x62\x69\x6e\x89\xe3\x31\xd2\x52\x53\x89\xe1\xb8\x0b\x00\x00\x00\xcd\x80
```

