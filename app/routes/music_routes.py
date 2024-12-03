from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.services.music_service import MusicService
from app.schemas.song_schema import Song
from pygame import mixer
import os

router = APIRouter(prefix="/music", tags=["Music Player"])

# Instância do serviço
music_service = MusicService()

# Modelo para receber o volume
class VolumeRequest(BaseModel):
    volume: float

@router.post("/play/")
async def play_song(song: Song):
    """
    Reproduz uma música a partir do caminho fornecido.
    """
    try:
        # Verifica se o caminho foi fornecido
        if not song.path:
            raise HTTPException(status_code=400, detail="File path is required.")
        
        # Verifica se o arquivo existe no caminho fornecido
        if not os.path.isfile(song.path):
            raise HTTPException(status_code=404, detail="File not found.")

        # Tenta reproduzir a música
        return music_service.play_song(song.path)

    except HTTPException as e:
        raise e  # Repassa exceções HTTP como estão
    except Exception as e:
        # Log detalhado para debug
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.post("/play/upload/")
async def upload_and_play_song(file: UploadFile = File(...)):
    """Faz upload de uma música e a reproduz"""
    try:
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
