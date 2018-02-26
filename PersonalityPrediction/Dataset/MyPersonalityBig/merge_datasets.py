import pandas as pd

# '', 'messageid', 'userid', 'message', 'updated_time', 'nchar'
types = {'userid':str, 'message':str}
posts = pd.read_csv("D:\Downloads\MyPersonalityBig\status_updates.csv", quotechar='"', usecols=[2,3], dtype=types, error_bad_lines=False, engine='python')
print("Status updates loaded.")

# 'userid', 'ope', 'con', 'ext', 'agr', 'neu', 'item_level', 'blocks', 'date'
types = {'userid':str, 'ope':float, 'con':float, 'ext':float, 'agr':float, 'neu':float}
big5 = pd.read_csv("D:\Downloads\MyPersonalityBig\/big5.csv", quotechar='"', usecols=[0,1,2,3,4,5], dtype=types)
print("Big Five scores loaded.")

df = big5.set_index('userid').join(posts.set_index('userid'), how='inner')
print("Join done.")

df.to_csv('join.csv')
print("Csv file written.")
