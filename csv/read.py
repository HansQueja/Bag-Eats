import sqlite3
import pandas as pd

df = pd.read_csv('food.csv', index_col=False)

print(df)

df.columns = df.columns.str.strip()

connection = sqlite3.connect('food.db')

df.to_sql('food_list', connection, if_exists='replace', index=False)