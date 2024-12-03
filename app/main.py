from fastapi import FastAPI
from app.routes.music_routes import router as music_router

app = FastAPI(title="Music Player API")

# Registra as rotas
app.include_router(music_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
