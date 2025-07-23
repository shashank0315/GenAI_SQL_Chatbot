import google.generativeai as genai

genai.configure(api_key="AIzaSyCLMkN_Iio8v8hjxzzSmZxGCiENJ1R_fRo")

# Use the recommended setup for Gemini 1.5
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# def get_sql_query(user_question):
#     prompt = f"""
# You are an AI that converts questions into SQLite queries.

# The database has a table named `total_sales` with columns: id, product_name, total_sales_amount, date.

# Only use valid column names in your SQL.

# Question: {user_question}
# Return only the SQL query.
# """

#     response = model.generate_content(prompt)
#     return response.text.strip()


def get_sql_query(user_question):
    prompt = f"""
You are an AI agent that converts questions into SQL queries for a SQLite database.

Use only the following table and column:
Table: total_sales
Columns: date, item_id, total_sales, total_units_ordered

User Question: {user_question}

Return ONLY the SQL query. Do NOT include markdown or code blocks.
"""
    response = model.generate_content(prompt)
    raw_sql = response.text.strip()

    # Remove backticks and markdown if LLM still adds it
    if "```" in raw_sql:
        raw_sql = raw_sql.replace("```sqlite", "").replace("```", "").strip()
    return raw_sql
