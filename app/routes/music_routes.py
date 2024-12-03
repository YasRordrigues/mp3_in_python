from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.music_service import MusicService
from app.schemas.song_schema import Song
import os

router = APIRouter(prefix="/music", tags=["Music Player"])

# Instância do serviço
music_service = MusicService()

@router.post("/play/")
async def play_song(song: Song):
    return music_service.play_song(song.path)

@router.post("/play/upload/")
async def upload_and_play_song(file: UploadFile = File(...)):
    """Faz upload de uma música e a reproduz"""
    try:
        # Salva o arquivo temporariamente
        temp_dir = "./temp/"
        os.makedirs(temp_dir, exist_ok=True)  # Cria a pasta se não existir
        file_path = os.path.join(temp_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Reproduz o arquivo salvo
        return music_service.play_uploaded_song(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading/playing song: {str(e)}")

@router.post("/pause/")
async def pause_song():
    return music_service.pause_song()

@router.post("/resume/")
async def resume_song():
    return music_service.resume_song()

@router.post("/volume/increase/")
async def increase_volume():
    return music_service.increase_volume()

@router.post("/volume/decrease/")
async def decrease_volume():
    return music_service.decrease_volume()

@router.post("/stop/")
async def stop_song():
    return music_service.stop_song()
