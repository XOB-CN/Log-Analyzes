blk_rulelist = ['a','b']

line = 'cc'

for blk_rule in blk_rulelist:
    if blk_rule in line:
        break

    print(line)