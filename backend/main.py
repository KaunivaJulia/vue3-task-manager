# главный файл бэкенда (создаётся FastAPI-приложение, описываются маршруты (эндпоинты) для CRUD,реализуется чтение/запись данных в tasks.json)

import json 
from pathlib import Path  # работа с путями к файлам
from typing import List  # типизация списков
from datetime import datetime  # чтобы проставлять дату создания

from fastapi import FastAPI, HTTPException  # FastAPI — сервер,  HTTPException — ошибки типа 404
from fastapi.middleware.cors import CORSMiddleware  # чтобы фронт мог обращаться к серверу 

from models import Task, TaskCreate, TaskUpdate

#путь к файлу tasks.json
DATA_FILE = Path(__file__).parent / "tasks.json"

# Создаём приложение FastAPI
app = FastAPI(title="Task Manager API")

# CORS нужен, тк фронтенд будет работать на http://localhost:5173
# бэкенд на http://localhost:8000
# Это разные "источники" (origins), браузер блокирует запросы без разрешения
# Поэтому мы добавляем middleware, который разрешает запросы с фронта
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

#Работа с данными (tasks.json) 


def read_tasks_raw() -> List[dict]:
    if not DATA_FILE.exists():
        # Если файла нет, создаём пустой
        DATA_FILE.write_text("[]", encoding="utf-8")

    # Читаем текст файла
    text = DATA_FILE.read_text(encoding="utf-8").strip()

    # Если файл пустой, считаем что задач нет
    if not text:
        return []

    # Преобразуем JSON-строку в Python-объект (список)
    return json.loads(text)


def write_tasks_raw(tasks: List[dict]) -> None:
    """
    Записываем список задач обратно в tasks.json. делаем запись после каждого изменения,
    чтобы студент мог открыть файл и увидеть актуальные данные
    """
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),  # красивое форматирование JSON
        encoding="utf-8"
    )


def next_id(tasks: List[dict]) -> int:
    """
    Вычисляем следующий id:
    - если задач нет -> id = 1
    - иначе -> max(id) + 1
    """
    return 1 if not tasks else max(t["id"] for t in tasks) + 1


# CRUD

# READ (получить все задачи)
@app.get("/api/tasks", response_model=List[Task])
def get_tasks():
    """
    GET /api/tasks
    Возвращает список всех задач.
    """
    return read_tasks_raw()


# READ (получить одну задачу по id)
@app.get("/api/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """
    GET /api/tasks/{id}
    Возвращает одну задачу по id.
    """
    tasks = read_tasks_raw()
    for t in tasks:
        if t["id"] == task_id:
            return t

    # Если не нашли -> 404
    raise HTTPException(status_code=404, detail="Task not found")


# CREATE (создать задачу)
@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    """
    POST /api/tasks
    Создаёт новую задачу

    payload (TaskCreate) приходит из тела запроса (JSON)
    FastAPI сам проверит поля по models.py (валидация)
    """
    tasks = read_tasks_raw()

    # model_dump() превращает Pydantic-модель в обычный dict
    task = payload.model_dump()

    # добавляем id и дату создания на сервере
    task["id"] = next_id(tasks)
    task["created_at"] = datetime.utcnow().isoformat()

    # добавляем задачу в список
    tasks.append(task)

    # записываем обратно в tasks.json
    write_tasks_raw(tasks)

    return task


# UPDATE (обновить задачу по id)
@app.put("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate):
    """
    PUT /api/tasks/{id}
    Обновляет существующую задачу.
    """
    tasks = read_tasks_raw()

    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            updated = payload.model_dump()
            updated["id"] = task_id
            updated["created_at"] = t.get("created_at", datetime.utcnow().isoformat())

            # заменяем задачу в списке
            tasks[i] = updated

            # пишем в файл
            write_tasks_raw(tasks)

            return updated

    raise HTTPException(status_code=404, detail="Task not found")


# DELETE (удалить задачу по id)
@app.delete("/api/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """
    DELETE /api/tasks/{id}
    Удаляет задачу.
    """
    tasks = read_tasks_raw()

    # оставляем только те, у кого id не равен task_id
    new_tasks = [t for t in tasks if t["id"] != task_id]

    # если длина не изменилась -> значит ничего не удалили -> задачи с таким id не было
    if len(new_tasks) == len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")

    # записываем новый список
    write_tasks_raw(new_tasks)

    # 204 означает "успешно, но без тела ответа"
    return None