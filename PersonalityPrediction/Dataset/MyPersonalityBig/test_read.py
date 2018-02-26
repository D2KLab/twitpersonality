import pandas as pd

types = {"userid":str,"ope":float,"con":float,"ext":float,"agr":float,"neu":float,"message":str}
df = pd.read_csv("join.csv", usecols=[0,1,2,3,4,5,6], dtype=types, error_bad_lines=False, engine="python")
print("\nDataframe correctly laoded.")
print(df.count())