import pandas as pd
import numpy as np
from mod.tools.io_mongo import MongoDB

sess = MongoDB()
mydb = sess.get_mongo_sess('20190708220011', 'system_txt')

# 将 MongoDB 的数据转换成 Pandas 的数据
mo_data = mydb.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})
pd_data = pd.DataFrame(list(mo_data))
del pd_data['_id']

# 开始构造最终数据
data_index = pd_data.log_time
data = pd.Series(np.arange(len(data_index)), index=data_index)
print(data)
print(data.resample('3600min'))