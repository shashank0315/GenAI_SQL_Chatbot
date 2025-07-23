import pandas as pd
import sqlite3

conn = sqlite3.connect("ecommerce.db")

df_eligibility = pd.read_csv("eligibility.csv")
df_ad_sales = pd.read_csv("ad_sales.csv")
df_total_sales = pd.read_csv("total_sales.csv")

df_eligibility.to_sql("eligibility", conn, if_exists="replace", index=False)
df_ad_sales.to_sql("ad_sales", conn, if_exists="replace", index=False)
df_total_sales.to_sql("total_sales", conn, if_exists="replace", index=False)

conn.close()

print("All tables loaded into ecommerce.db")
