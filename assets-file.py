import json
import hashlib

files = []

fileName = open("assets.json", "r")
fileContent = fileName.read()
data = json.loads(fileContent)

md5 = hashlib.md5()
md5.update(bytes(fileContent, 'utf-8'))
hashedData = md5.hexdigest()

version = data['version']
files.extend(data['files'])
size = 0

for p in range(len(files)):
    size += files[p]['packedsize']
    
print('Version: ' + str(version) + '\r\n' + 'Size: ' + str("{:,}".format(size)) + '\r\n' + 'Hash: ' + hashedData)
