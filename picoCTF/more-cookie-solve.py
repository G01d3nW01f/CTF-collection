#!/usr/bin/python3

import requests
import base64

url = "http://mercury.picoctf.net:25992/"

s = requests.Session()
s.get(url)

cookie = s.cookies["auth_name"]
decoded_cookie = base64.b64decode(cookie)
raw_cookie = base64.b64decode(decoded_cookie)


def exploit():

    for i in range(0,len(raw_cookie)):
        for j in range(0,8):
            bit_flip_guess = (
                    raw_cookie[0:i]
                    + ((raw_cookie[i] ^ (1 << j)).to_bytes(1,"big"))
                    + raw_cookie[i + 1 :]
            )
            guess = base64.b64encode(base64.b64encode(bit_flip_guess)).decode()
            r = requests.get(url, cookies={"auth_name": guess})
            print(f"[+]Trying.... : {guess}")
            if "picoCTF{" in r.text:
                print(f"Admin bit found!!! in byte {i} bit {j}.")
                print("Flag: "+r.text.split("<code>")[1].split("</code>")[0])
                return
exploit()
