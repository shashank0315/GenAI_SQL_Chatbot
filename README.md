# GenAI_SQL_Chatbot
 ## ⚙️ Features
- Ask questions like "What is my total sales?" or "Which product had the highest CPC?"
- Auto-generates SQL using Gemini API
- Executes SQL on SQLite database
- Visualizes results using Chart.js
- Clean, responsive frontend
## 🧰 Tech Stack
- **Backend**: FastAPI, SQLite3, Gemini API (Google Generative AI)
- **Frontend**: HTML + CSS + Chart.js
- **Database**: total_sales.db
- **Language**: Python

## 🗂 Project Structure
main.py
llm_utils.py
query_executor.py
test_llm.py
check_answers.py
/static/index.html
/data/total_sales.db


## 🚀 Setup Instructions
```bash
git clone https://github.com/shashank0315/GenAI_SQL_Chatbot.git
cd GenAI_SQL_Chatbot

python -m venv venv
venv\Scripts\activate     # For Windows
# OR
source venv/bin/activate  # For macOS/Linux

pip install -r requirements.txt
```


## to run the project
uvicorn main:app --reload


