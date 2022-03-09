import requests
import http.client
with open("hey.txt", "r+") as f:
    http.client._MAXLINE = 99999999999999999
    t = f.read()
    r = requests.get(
        f"http://127.0.0.1:5000/main/VIT/imnaveed2003@gmail.com/{t}")


print(r.content)
