import os
from pygame import mixer

class MusicService:
    def __init__(self):
        mixer.init()
        self.current_volume = 0.5
        self.current_song = None

    def play_song(self, path: str):
        try:
            # Carrega e reproduz a música especificada
            mixer.music.load(path)
            mixer.music.set_volume(self.current_volume)
            mixer.music.play()
            self.current_song = path  # Define a música atual
            return {"message": f"Playing: {os.path.basename(path)}"}
        except Exception as e:
            raise Exception(f"Error playing song: {str(e)}")

    def pause_song(self):
        try:
            mixer.music.pause()
            return {"message": "Music paused"}
        except Exception as e:
            raise Exception(f"Error pausing song: {str(e)}")

    def resume_song(self):
        try:
            mixer.music.unpause()
            return {"message": "Music resumed"}
        except Exception as e:
            raise Exception(f"Error resuming song: {str(e)}")

    def stop_song(self):
        try:
            mixer.music.stop()
            self.current_song = None
            return {"message": "Music stopped"}
        except Exception as e:
            raise Exception(f"Error stopping song: {str(e)}")
