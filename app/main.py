from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.music_routes import router as music_router

app = FastAPI(title="Music Player API")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permita o acesso apenas do frontend local
    allow_credentials=True,
    allow_methods=["*"],  # Permita todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permita todos os cabeçalhos
)

# Registra as rotas
app.include_router(music_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
