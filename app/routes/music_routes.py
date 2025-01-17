from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.music_service import MusicService
from pygame import mixer
from typing import List
import os

router = APIRouter(prefix="/music", tags=["Music Player"])

# Instância do serviço
music_service = MusicService()

# Modelo para receber o volume
class VolumeRequest(BaseModel):
    volume: float

# Modelo para receber o nome da música
class SongRequest(BaseModel):
    song_name: str

# Diretório onde as músicas serão armazenadas
UPLOAD_DIR = "./uploaded_songs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/")
async def upload_songs(files: List[UploadFile] = File(...)):
    """Faz upload de múltiplas músicas"""
    uploaded_files = []
    try:
        for file in files:
            file_path = os.path.join(UPLOAD_DIR, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            uploaded_files.append(file.filename)
        return {"message": "Files uploaded successfully", "files": uploaded_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")


@router.get("/list/")
async def list_songs():
    """Retorna uma lista de músicas disponíveis"""
    try:
        songs = os.listdir(UPLOAD_DIR)
        return {"songs": songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing songs: {str(e)}")


@router.post("/play/")
async def play_song(song: SongRequest):
    """Reproduz ou retoma uma música"""
    try:
        file_path = os.path.join(UPLOAD_DIR, song.song_name)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Song not found")
        return music_service.play_song(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error playing song: {str(e)}")


@router.post("/pause/")
async def pause_song():
    return music_service.pause_song()


@router.post("/volume/set/")
async def set_volume(request: VolumeRequest):
    """Define o volume diretamente."""
    volume = request.volume
    if not 0.0 <= volume <= 1.0:
        raise HTTPException(status_code=400, detail="Volume must be between 0 and 1.")
    try:
        music_service.current_volume = volume
        mixer.music.set_volume(volume)
        return {"message": f"Volume set to {volume}", "volume": volume}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error setting volume: {str(e)}")


@router.post("/volume/increase/")
async def increase_volume():
    if music_service.current_volume >= 1.0:
        return {"message": "Volume is already at maximum", "volume": music_service.current_volume}
    music_service.current_volume = round(music_service.current_volume + 0.1, 1)
    mixer.music.set_volume(music_service.current_volume)
    return {"message": f"Volume increased to {music_service.current_volume}", "volume": music_service.current_volume}


@router.post("/volume/decrease/")
async def decrease_volume():
    if music_service.current_volume <= 0.0:
        return {"message": "Volume is already at minimum", "volume": music_service.current_volume}
    music_service.current_volume = round(music_service.current_volume - 0.1, 1)
    mixer.music.set_volume(music_service.current_volume)
    return {"message": f"Volume decreased to {music_service.current_volume}", "volume": music_service.current_volume}


@router.post("/stop/")
async def stop_song():
    return music_service.stop_song()
