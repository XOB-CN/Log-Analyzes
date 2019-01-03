aa = ['1h','2h','3h','4h','5h','6h','7h','8h','9h','10h']
import copy

n = 0
m = 0
log_evet = []
queue = []
for line in aa:
    n += 1
    m += 1
    log_evet.append([n,line])

    if m == 3:
        log_evet_copy = copy.deepcopy(log_evet)
        queue.append(log_evet_copy)
        log_evet.clear()
        m = 0

queue.append(log_evet)

print(queue)