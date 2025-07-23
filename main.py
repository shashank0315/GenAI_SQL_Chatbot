from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from llm_utils import get_sql_query
from db_utils import run_query
from response_formatter import format_response
import pandas as pd

app = FastAPI(docs_url=None, redoc_url=None)  # Disable Swagger UI

class QuestionInput(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(input: QuestionInput):
    question = input.question.lower()
    # Detect CPC or RoAS questions
    if "cpc" in question:
        df = pd.read_csv("ad_sales.csv")
        df = df[df["clicks"] > 0]
        df["cpc"] = df["ad_spend"] / df["clicks"]
        idx = df["cpc"].idxmax()
        row = df.loc[idx]
        result = [{"item_id": int(row["item_id"]), "cpc": round(row["cpc"], 2)}]
        answer = f"Product {int(row['item_id'])} had the highest CPC: ${row['cpc']:.2f}"
        sql = "SELECT item_id, ad_spend * 1.0 / clicks AS cpc FROM ad_sales WHERE clicks > 0 ORDER BY cpc DESC LIMIT 1;"
        return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": {"type": "bar", "x": [int(row["item_id"])], "y": [round(row["cpc"], 2)], "label": "CPC ($)"}}
    elif "roas" in question or "return on ad spend" in question:
        df = pd.read_csv("ad_sales.csv")
        df = df[df["ad_spend"] > 0]
        df["roas"] = df["ad_sales"] / df["ad_spend"]
        top = df.sort_values("roas", ascending=False).head(10)
        result = top[["item_id", "roas"]].to_dict(orient="records")
        answer = "Top 10 products by RoAS (Return on Ad Spend)"
        sql = "SELECT item_id, ad_sales * 1.0 / ad_spend AS roas FROM ad_sales WHERE ad_spend > 0 ORDER BY roas DESC LIMIT 10;"
        return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": {"type": "bar", "x": top["item_id"].astype(int).tolist(), "y": top["roas"].round(2).tolist(), "label": "RoAS"}}
    elif "total sales" in question:
        df = pd.read_csv("total_sales.csv")
        # Detect if user wants a sum or a group by
        if "by date" in question:
            grouped = df.groupby("date")["total_sales"].sum().reset_index()
            x = grouped["date"].tolist()
            y = grouped["total_sales"].round(2).tolist()
            label = "Total Sales ($)"
            sql = "SELECT date, SUM(total_sales) AS total_sales FROM total_sales GROUP BY date;"
            result = grouped.to_dict(orient="records")
            answer = "Total sales by date"
            return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": {"type": "bar", "x": x, "y": y, "label": label}}
        elif "by item" in question or "per item" in question or "each item" in question:
            grouped = df.groupby("item_id")["total_sales"].sum().reset_index()
            x = grouped["item_id"].astype(str).tolist()
            y = grouped["total_sales"].round(2).tolist()
            label = "Total Sales ($)"
            sql = "SELECT item_id, SUM(total_sales) AS total_sales FROM total_sales GROUP BY item_id;"
            result = grouped.to_dict(orient="records")
            answer = "Total sales by item"
            return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": {"type": "bar", "x": x, "y": y, "label": label}}
        else:
            total = df["total_sales"].sum()
            sql = "SELECT sum(total_sales) FROM total_sales;"
            result = [{"sum(total_sales)": round(total, 2)}]
            answer = f"Answer: {round(total, 2)}"
            return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": {"type": "pie", "x": ["Total Sales"], "y": [round(total, 2)], "label": "Total Sales ($)"}}
    else:
        sql = get_sql_query(question)
        result = run_query(sql)
        answer = format_response(question, result)
        # Try to visualize if result is a list of dicts with at least 2 columns
        chart = None
        if isinstance(result, list) and len(result) > 1 and isinstance(result[0], dict):
            keys = list(result[0].keys())
            if len(keys) >= 2:
                x = [row[keys[0]] for row in result]
                y = [row[keys[1]] for row in result]
                chart = {"type": "bar", "x": x, "y": y, "label": keys[1]}
        return {"question": question, "sql": sql, "result": result, "answer": answer, "chart": chart}

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
