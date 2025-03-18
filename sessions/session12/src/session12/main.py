import os
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

api = FastAPI(
    title="TODO Etic_Algarve API"
)

DB_USER = os.getenv("DB_USER",None)
DB_PASSWORD = os.getenv("DB_PASSWORD",None)
DB_HOST = os.getenv("DB_HOST",None)
DB_PORT = os.getenv("DB_PORT",None)
DB_NAME = os.getenv("DB_NAME",None)

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

SQLModel.metadata.create_all(engine)

@api.get("/task")
def list_tasks():pass

@api.post("/task")
def create_task():pass

@api.put("/task")
def edit_task():pass

@api.patch("/task")
def close_task():pass

@api.delete("/task")
def delete_task():pass

