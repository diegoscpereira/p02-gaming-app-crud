from fastapi import FastAPI
import backend.models as m
from backend.database import engine
from backend.routers.explore import router as re
from backend.routers.library import router as rl

m.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Games API")
app.include_router(re)
app.include_router(rl)