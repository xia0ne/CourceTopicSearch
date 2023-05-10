import uvicorn
from fastapi import FastAPI
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="./templates")


def make_db_connection():
    conn = sqlite3.connect("src/182Wquestion.db")
    cursor = conn.cursor()
    return conn, cursor


@app.on_event("startup")
async def startup():
    app.db_connection = make_db_connection()


@app.get("/search")
async def search(q: str):
    cursor = app.db_connection[1]
    sql = "SELECT * FROM lists WHERE question LIKE ?"
    keyword = f"%{q}%"
    cursor.execute(sql, (keyword,))
    result = cursor.fetchall()
    if len(result) == 0:
        return "Sorry, No related issues found!"
    ans = ["Find {} related issues in total".format(len(result))]
    ans = [{"Source": "无" if i[2] == "undefined" else i[2], "Q": i[5], "A": i[4]} for i in result]
    return ans

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



if __name__ == "__main__":
    uvicorn.run(app='app:app', host="127.0.0.1", port=8000)
