from fastapi import APIRouter, HTTPException
from app.services.music_service import MusicService
from app.schemas.song_schema import Song

router = APIRouter(prefix="/music", tags=["Music Player"])

# Instância do serviço
music_service = MusicService()

@router.post("/play/")
async def play_song(song: Song):
    return music_service.play_song(song.path)

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
