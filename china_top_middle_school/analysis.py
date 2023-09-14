import pandas as pd

df = pd.read_csv('zhongxue.csv')

province_counts = df.groupby('省份')['学校名称'].count().reset_index(name='数量')

top_provinces = province_counts.sort_values('数量', ascending=False).head(15)
top_provinces.index = range(1, len(top_provinces) + 1)
print(top_provinces)

for pro in ["浙江", "吉林", "湖南"]:
    pro_ranks = df[df['省份'] == pro].sort_values('省内排序')
    pro_ranks.index = range(1, len(pro_ranks) + 1)
    pro_ranks = pro_ranks.loc[:, ["排名", "省份", "省内排序", "学校名称"]]
    print("-" * 60)
    print(pro_ranks)

