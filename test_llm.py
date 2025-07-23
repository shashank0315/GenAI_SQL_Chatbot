from llm_utils import get_sql_query
from db_utils import run_query

q = "What is my total sales?"
print("User Question:", q)

sql = get_sql_query(q)
print("SQL Generated:\n", sql)

result = run_query(sql)
print("Query Result:\n", result)

from db_utils import show_columns

columns = show_columns("total_sales")
print("Columns in total_sales table:")
for col in columns:
    print(f" - {col[1]}")


