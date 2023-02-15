import urllib.request
import base64
import hmac
import time

APIURL = "https://api-swap-rest.bingbon.pro"
APIKEY = "2Ohbn3NBvAiBSAbjtwzAKMOXvpcSqCtdXxqK9XFHF56ouSjcai56CHydcFpI0g5IStjh3GbGd9YftZAIew"
SECRETKEY = "RgVYyNap7rCIa5mkD5DehhcIPnoIdeJvIJ89kBOL4sMs94sKxMqfQydrGhJofRGSSVY5Go6vmXZvIKrvhMLXg"

def genSignature(path, method, paramsMap):
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr = method + path + paramsStr
    return hmac.new(SECRETKEY.encode("utf-8"), paramsStr.encode("utf-8"), digestmod="sha256").digest()

def post(url, body):
    req = urllib.request.Request(url, data=body.encode("utf-8"), headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req).read()

def getBalance():
    paramsMap = {
        "apiKey": APIKEY,
        "timestamp": int(time.time()*1000),
        "currency": "USDT"
    }
    sortedKeys = sorted(paramsMap)
    paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
    paramsStr += "&sign=" + urllib.parse.quote(base64.b64encode(genSignature("/api/v1/user/getBalance", "POST", paramsMap)))
    url = "%s/api/v1/user/getBalance" % APIURL
    return post(url, paramsStr)


def main():
    print(getBalance())


if __name__ == '__main__':
    main()