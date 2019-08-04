import os, re
data = r'''E:\05.编程区\GitHub\Log-Analyzes\temp\log/configserver/licensemgr.log.1'''

file = os.path.basename(data)
print(file.split('.')[0])