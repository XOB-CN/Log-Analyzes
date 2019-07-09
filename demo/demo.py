import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

s = pd.Series([1,2,3,np.nan,6,8])

datas = pd.date_range('20170101',periods=7)
df = pd.DataFrame(np.random.randn(7,4), index=datas, columns=list('QWER'))

demo = pd.Series(['A','B','V','C','C'])

print(demo.value_counts())