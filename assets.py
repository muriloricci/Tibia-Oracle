import json
import requests
import hashlib
import os.path
import tweepy
import twitterSecrets

files = []
versionFileName = 'version.txt'

# Open file with hash version
if os.path.isfile(versionFileName):
    versionFile = open(versionFileName, 'r')
    versionR = versionFile.read()
else:
    versionR = ''

# Read json from URL
fileName = 'https://static.tibia.com/launcher/assets-current/assets.json'
packageName = 'https://static.tibia.com/launcher/tibiaclient-windows-current/package.json'

f = requests.get(fileName)
data = json.loads(f.text)

p = requests.get(packageName)
pdata = json.loads(p.text)

# Hash json with MD5 method
md5 = hashlib.md5()
md5.update(bytes(f.text, 'utf-8'))
hashedData = md5.hexdigest()

version = pdata['version']
files.extend(data['files'])
size = 0

# Sum file sizes
for p in range(len(files)):
    size += files[p]['packedsize']

# Compare hash strings
if versionR != hashedData:
    versionText = 'New @Tibia patch detected! #Tibia'

    # Write hash to version.txt
    versionW = open(versionFileName, 'w')
    versionW.write(hashedData)
    versionW.close()

    auth = tweepy.OAuthHandler(twitterSecrets.apiKey, twitterSecrets.apiKeySecret)
    auth.set_access_token(twitterSecrets.accessToken, twitterSecrets.accessTokenSecret)
    
    api = tweepy.API(auth)
    
    api.update_status(versionText + '\r\n\n' + 'Version: ' + str(version))
else:
    versionText = ''
    
print('Version: ' + str(version) + '\r\n' + 'Size: ' + str("{:,}".format(size)) + '\r\n' + 'Hash: ' + hashedData + '\r\n' + versionText)
