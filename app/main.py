from app.routers import checking, root, code_generator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(root.router)
app.include_router(checking.router)
app.include_router(code_generator.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
