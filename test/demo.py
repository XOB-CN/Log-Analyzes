line = '&lt;Host&gt;&lt;![CDATA[10.91.3.51]]&gt;&lt;/Host&gt;'

print(line.split('[')[-1].split(']')[0])