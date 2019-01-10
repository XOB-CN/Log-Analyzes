import zipfile

def unzip(filename):
    zip_file = zipfile.ZipFile(filename)
    zip_file.extractall('temp')

unzip('Agent_10100-30001_01-10-2019_15-54.zip')