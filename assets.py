import json
import requests
import hashlib

files = []

fileName = 'https://static.tibia.com/launcher/assets-current/assets.json'

f = requests.get(fileName)
data = json.loads(f.text)

md5 = hashlib.md5()
md5.update(bytes(f.text, 'utf-8'))
hashedData = md5.hexdigest()

version = data['version']
files.extend(data['files'])
size = 0

for p in range(len(files)):
    size += files[p]['packedsize']
    
print('Version: ' + str(version) + '\r\n' + 'Size: ' + str("{:,}".format(size)) + '\r\n' + 'Hash: ' + hashedData)
