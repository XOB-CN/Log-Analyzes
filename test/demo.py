
for i in range(10):
    n = 0
    m = 0
    for y in range(3):
        m += 1

        if m>2:
            n+=1
            m=0

    n += 1

print(n)