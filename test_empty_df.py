import pandas as pd
df1 = pd.DataFrame(columns=['a', 'b'])
print(df1.empty)
df2 = df1.copy() if not df1.empty else pd.DataFrame()
print(df2.columns)
df3 = df1.copy()
print(df3.columns)
