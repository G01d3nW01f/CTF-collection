Secured Session

Source Code:
```
import os
from flask import Flask, request, session
from flag import flag

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def secret_key_to_int(s):
    try:
        secret_key = int(s)
    except ValueError:
        secret_key = 0
    return secret_key

@app.route("/flag")
def index():
    secret_key = secret_key_to_int(request.args['secret_key']) if 'secret_key' in request.args else None
    session['flag'] = flag
    if secret_key == app.config['SECRET_KEY']:
      return session['flag']
    else:
      return "Incorrect secret key!"

@app.route('/')
def source():
    return "

%s

" % open(__file__).read()

if __name__ == "__main__":
    app.run()
```

key is generated in functions
these are import the flag to session (cookie)

![image](https://user-images.githubusercontent.com/75846902/203549978-d457abfb-ebe9-41ca-bd80-647d7ffb3497.png)

![image](https://user-images.githubusercontent.com/75846902/203550080-fbeecad3-3f27-4007-8a94-96869c391b16.png)

copy the sessions value and paste to jwt.io

![image](https://user-images.githubusercontent.com/75846902/203550330-58678e9b-33b6-4cce-bfd2-54e3b833b667.png)

looks like base64...

so decode from base64
```
->$ echo "MjQ3Q1RGe2RhODA3OTVmOGE1Y2FiMmUwMzdkNzM4NTgwN2I5YTkxfQ==" | base64 --decode
247CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx}
```



