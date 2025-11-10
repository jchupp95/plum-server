from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import user
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.include_router(user.router, prefix="/users", tags=["Users"])