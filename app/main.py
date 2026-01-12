from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Allow frontend (React/Next.js) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Welcome to Juris-Cape API", "docs": "/docs", "health_check": f"{settings.API_PREFIX}/"}

# This is just for debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)