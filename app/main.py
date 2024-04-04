from fastapi import FastAPI
from .database import Base, engine
from .routes import auth, user

Base.metadata.create_all(engine)

app = FastAPI(
    title='FastAPI with JWT authentication',
    version='1.0.0',
    docs_url='/docs'
)

app.include_router(router=auth.router, prefix='/api')
app.include_router(router=user.router, prefix='/api')