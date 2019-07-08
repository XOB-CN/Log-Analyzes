import pandas as pd
from mod.tools.io_mongo import MongoDB

sess = MongoDB()
mydb = sess.get_mongo_sess('20190708220011', 'system_txt')

# 将 MongoDB 的数据转换成 Pandas 的数据
mo_data = mydb.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})
pd_data = pd.DataFrame(list(mo_data))
del pd_data['_id']

# 对数据做进一步的处理
# data = pd_data[['log_time','log_component']]

# 开始构造最终数据
# 确定数据中包含的最大时间
time_max = pd_data['log_time'].max()
# 确定数据中包含的最小时间
time_min = pd_data['log_time'].min()

print(pd_data[['log_time','log_component']])