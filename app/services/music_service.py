import os
from pygame import mixer

class MusicService:
    def __init__(self):
        mixer.init()
        self.current_volume = 0.5
        self.current_song = None

    def play_song(self, path: str):
        try:
            mixer.music.load(path)  # Carrega a música
            mixer.music.set_volume(self.current_volume)  # Define o volume
            mixer.music.play()  # Inicia a reprodução
            self.current_song = path  # Atualiza a música atual
            return {"message": f"Playing: {os.path.basename(path)}"}
        except Exception as e:
            raise Exception(f"Error playing song: {str(e)}")

    def play_uploaded_song(self, file_path: str):
        """
        Reproduz uma música salva no servidor.
        """
        return self.play_song(file_path)

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
            return {"message": "Music stopped"}
        except Exception as e:
            raise Exception(f"Error stopping song: {str(e)}")
