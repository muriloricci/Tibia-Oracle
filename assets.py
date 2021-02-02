import json
import requests
import hashlib
import os.path
import tweepy
import secrets

# Variables, reading from JSONs and hashes
versionHash = 'version.txt'
if os.path.isfile(versionHash):
    versionFile = open(versionHash, 'r')
    versionFileRead = versionFile.read()
    versionFile.close()
else:
    versionFileRead = ''

assets = 'https://static.tibia.com/launcher/assets-current/assets.json'
package = 'https://static.tibia.com/launcher/tibiaclient-windows-current/package.json'

assetsFile = requests.get(assets)
assetsData = json.loads(assetsFile.text)

packageFile = requests.get(package)
packageData = json.loads(packageFile.text)

md5 = hashlib.md5()
md5.update(bytes(assetsFile.text, 'utf-8'))
assetsHash = md5.hexdigest()

version = packageData['version']
build = assetsData['version']

assetsFiles = assetsData['files']
assetsFilesSize = 0

# Looping files to sum values
for p in range(len(assetsFiles)):
    assetsFilesSize += assetsFiles[p]['packedsize']

# Comparing hashes and tweeting if different
if assetsHash != versionFileRead:
    versionFileWrite = open(versionHash, 'w')
    versionFileWrite.write(assetsHash)
    versionFile.close()
    
    auth = tweepy.OAuthHandler(secrets.apiKey, secrets.apiKeySecret)
    auth.set_access_token(secrets.accessToken, secrets.accessTokenSecret)
    api = tweepy.API(auth)
    
    api.update_status('New patch available for @Tibia! #Tibia' + '\r\n\n' 
        + '🔸 Version: ' + str(version) + ' 🆕')
    print('New patch available for @Tibia! #Tibia' + '\r\n'
        + 'Version: ' + str(version) + ' (' + str(build) + ')' + '\r\n'
        + 'Assets size: ' + str("{:,}".format(assetsFilesSize)))
else:
    print('Version: ' + str(version) + ' (' + str(build) + ')'  + '\r\n'
        + 'Assets size: ' + str("{:,}".format(assetsFilesSize)))
