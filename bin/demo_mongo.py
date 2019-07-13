import pandas as pd
import matplotlib.pyplot as plt
from mod.tools.io_mongo import MongoDB

sess = MongoDB()
mydb = sess.get_mongo_sess('20190713131741', 'default')

# 将 MongoDB 的数据转换成 Pandas 的数据
mo_data = mydb.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})
pd_data = pd.DataFrame(list(mo_data))
del pd_data['_id']

# 开始处理 pandas 数据
tmp1_data = pd_data.set_index('log_time')
tmp2_data = tmp1_data.log_weight.resample('T').sum()
tmp3_data = tmp2_data[tmp2_data.values > 0]

# 绘制图表：基于时间的事件总数
plt.bar(tmp3_data.index, tmp3_data)
plt.show()
