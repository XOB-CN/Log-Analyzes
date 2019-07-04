import pandas as pd
from mod.tools.io_mongo import MongoDB

sess = MongoDB()
mydb = sess.get_mongo_docs('20190702162300', 'system_txt')

# 将 MongoDB 的数据转换成 Pandas 的数据
mo_data = mydb.find({'$or':[{'log_level':'WRN'},{'log_level':'ERR'}]})
pd_data = pd.DataFrame(list(mo_data))
del pd_data['_id']

# 对数据做进一步的处理
data = pd_data[['log_time','log_component']]

# # 开始绘图
# import matplotlib.pyplot as plt
# x = [1,2,3,4]
# y = [1,2,0,0]
#
# plt.plot(x,y)
# plt.show()

print(pd_data)