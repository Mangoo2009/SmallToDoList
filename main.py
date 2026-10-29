import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from DataBase import Session, ToDoList

load_dotenv()

templates = Jinja2Templates(directory='templates')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def main(request: Request):
    with Session() as session:
        tasks = session.query(ToDoList).all()
    return templates.TemplateResponse(
        request,
        "Main.html",
        {"tasks": tasks}
    )

@app.post('/delete/{task_id}')
def delete(request: Request, task_id: int):
    with Session() as session:
        task = session.query(ToDoList).filter(ToDoList.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
    return RedirectResponse(url='/', status_code=303)

@app.post('/edit/{task_id}')
def edit_task(
        request: Request,
        task_id: int,
        Zametka: str = Form(),
        Status: bool = Form(False)):
    with Session() as session:
        task = session.query(ToDoList).filter(ToDoList.id == task_id).first()
        if task:
            task.Zametka = Zametka
            task.Status = Status
            session.commit()
    return RedirectResponse(url='/', status_code=303)


@app.post('/')
def add_Zametka(
    request: Request,
    Zametka: str = Form(...),
    Status: bool = Form(False)
):
    with Session() as session:
        new_task = ToDoList(Zametka=Zametka, Status=Status)
        session.add(new_task)
        session.commit()

        tasks = session.query(ToDoList).all()

    return RedirectResponse(url='/', status_code=303)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)