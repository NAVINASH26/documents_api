
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth
from app.models.user import User
from app.models.document import Document 
from app.models.status_history import DocumentStatusHistory
from app.routes import documents

#print(Base.metadata.tables.keys())

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Document Management API")

app.include_router(auth.router)
app.include_router(documents.router)

@app.get("/")
def home():
    return {"message": "API running"}