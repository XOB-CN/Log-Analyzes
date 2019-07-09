import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mod.tools.io_mongo import MongoDB

sess = MongoDB()
mydb = sess.get_mongo_sess('20190708220011', 'system_txt')

# 将 MongoDB 的数据转换成 Pandas 的数据
mo_data = mydb.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})
pd_data = pd.DataFrame(list(mo_data))
del pd_data['_id']

# 开始构造最终数据
data_index = pd_data.log_time
data = pd.Series(np.random.randint(1,2,len(data_index)), index=data_index)
data = data.resample('T').sum()
data = data[data.values > 0]
print(data)

# 开始绘图
plt.bar(data.index, data.values)
plt.show()
