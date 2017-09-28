import urllib.request

url = "http://www.google.com"
headers = {}
headers['User-Agent'] = "Googlebot"
request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
print(response.read())
response.close()

