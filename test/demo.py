import zipfile
from mod.tools import LogAnalze

def unzip(filename):
    file_list = []
    zip_file = zipfile.ZipFile(filename)
    for name in zip_file.filelist:
        for rule in ['backup\.log','Database\.log']:
            if LogAnalze.match_any(rule, name.filename):
                file_list.append(name.filename)

    print(file_list)

unzip('Agent_10100-30001_01-10-2019_15-54.zip')