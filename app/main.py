from fastapi import FastAPI
from app.api.endpoints import auth, predictions, users
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(title=settings.PROJECT_NAME)

# Create database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(predictions.router, prefix="/predictions", tags=["predictions"])
app.include_router(users.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)