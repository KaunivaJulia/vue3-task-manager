# Описывается "модель" задачи: какие поля у задачи есть и какие типы данных

from pydantic import BaseModel, Field  # BaseModel — базовый класс модели, Field — дополнительные правила/ограничения
from typing import Literal  # Literal ограничивает значения строк (например, priority только "low/medium/high")

Priority = Literal["low", "medium", "high"]
Category = Literal["work", "study", "home", "other"]

class TaskBase(BaseModel):
# title — заголовок задачи (от 1 до 120 символов)
    title: str = Field(min_length=1, max_length=120)
# description — описание задачи (может быть пустым)
    description: str = Field(default="", max_length=2000)
# priority — приоритет: low/medium/high (по умолчанию медиум)
    priority: Priority = "medium"
# category — категория: work/study/home/other (по умолчанию other)
    category: Category = "other"
    important: bool = False
    completed: bool = False

class TaskCreate(TaskBase):
    #Модель для создания задачи (POST /api/tasks)
    pass

class TaskUpdate(TaskBase):
    #Модель для обновления задачи (PUT /api/tasks/{id})
    pass

class Task(TaskBase):
    #Модель задачи "как она хранится на сервере" и как отдаётся клиенту
    id: int
    created_at: str
