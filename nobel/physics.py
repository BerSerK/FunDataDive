import pandas as pd
import datetime as dt
import tabulate as tb

dfs = pd.read_html("https://en.wikipedia.org/wiki/List_of_Nobel_laureates_in_Physics")
df = dfs[0]
section_sep_width = 100
this_year = dt.datetime.now().year

def get_age(Laureate):
    if '(' not in Laureate:
        return None, True, None
    birth = Laureate.split('(')[1]
    expire = False
    if '–' in birth:
        birth_year = birth.split('–')[0]
        death_year = birth.split('–')[1]
        death_year = death_year.split(')')[0]
        birth = birth_year
        age = int(death_year) - int(birth_year)
        expire = True
    if 'b.' in birth:
        birth = birth.split("b.")[1].strip()[:-1]
        age = this_year - int(birth)
    birth = int(birth)
    return birth, expire, age

# rename column name containing "Laureate" to "Laureate"
for col in df.columns:
    if 'Laureate' in col:
        df.rename(columns={col: 'Laureate[A]'}, inplace=True)
    if 'Country' in col:
        df.rename(columns={col: 'Country[B]'}, inplace=True)

# remove useless rows, like the Country[B] containing "mw-parser-output"
df = df[df['Country[B]'].apply(lambda x: "mw-parser-output" not in x)]

print("总共有{}位诺贝尔物理学奖获得者.".format(df.shape[0]))
print("-" * section_sep_width)
# assign df['Laureate[A]'].apply(get_age) to  df['birth_expire']
df.loc[:, 'birth_expire'] = df['Laureate[A]'].apply(get_age)
df.loc[:, 'age'] = df['birth_expire'].apply(lambda x: x[2])
df.loc[:, 'expire'] = df['birth_expire'].apply(lambda x: x[1])

# 删除 age is None 的数据
df  = df[df['Country[B]'].apply(lambda x: "War" not in x)]

# 筛选出expire = False 中年龄最大的十位, 提取 Year, Laureate[A], Country[B], age 这几列.
df_head = df[df['expire'] == False].sort_values(by='age', ascending=False).head(10)
df_head.reindex()
df_head = df_head.loc[:, ['Year', 'Laureate[A]', 'Country[B]', 'age']]

print("# 年龄最大的十位 在世 诺贝尔物理学奖获得者.")
print(df_head)
print("-" * section_sep_width)

# 所有人中, 年龄最大的十位.
df_head = df.sort_values(by='age', ascending=False).head(10)
df_head = df_head.loc[:, ['Year', 'Laureate[A]', 'Country[B]', 'age', 'expire']]
print("# 所有人中, 年龄最大的十位.")
print(df_head)

# 计算每个国家有多少人. 有的人有多个国籍用sep分隔, 展开成多行再用 groupby 统计
sep = '\xa0'
# 使用copy()创建DataFrame的副本，以确保我们在副本上进行修改
df_copy = df.copy()
df_copy.loc[:, 'Country'] = df_copy['Country[B]'].apply(lambda x: x.split(sep))
df_country = df_copy.explode('Country')
# remove [xxx] in the country name
df_country['Country'] = df_country['Country'].apply(lambda x: x.split('[')[0])
df_country_count = df_country.groupby('Country').count().sort_values(by = 'Laureate[A]', ascending=False)
print("-" * section_sep_width, "\n", "# 诺贝尔物理学奖获得者国籍分布.")
# print(df_country_count) only keep columns we need
print(df_country_count.loc[:, ['Laureate[A]']])

print("-" * section_sep_width)
print("# 中国获奖者")
print(df_country[df_country['Country'] == 'Republic of China'].loc[:, ['Year', 'Laureate[A]', 'Country[B]']])