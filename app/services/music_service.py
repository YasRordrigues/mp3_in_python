from pygame import mixer

class MusicService:
    def __init__(self):
        mixer.init()
        self.current_volume = 0.5
        self.current_song = None

    def play_song(self, path: str):
        try:
            mixer.music.load(path)
            mixer.music.set_volume(self.current_volume)
            mixer.music.play()
            self.current_song = path
            return {"message": f"Playing: {path.split('/')[-1]}"}
        except Exception as e:
            raise Exception(f"Error playing song: {str(e)}")

    def pause_song(self):
        try:
            mixer.music.pause()
            return {"message": "Music paused"}
        except Exception:
            raise Exception("Error pausing song")

    def resume_song(self):
        try:
            mixer.music.unpause()
            return {"message": "Music resumed"}
        except Exception:
            raise Exception("Error resuming song")

    def increase_volume(self):
        if self.current_volume >= 1.0:
            return {"message": "Volume is already at maximum"}
        self.current_volume = round(self.current_volume + 0.1, 1)
        mixer.music.set_volume(self.current_volume)
        return {"message": f"Volume increased to {self.current_volume}"}

    def decrease_volume(self):
        if self.current_volume <= 0.0:
            return {"message": "Volume is already at minimum"}
        self.current_volume = round(self.current_volume - 0.1, 1)
        mixer.music.set_volume(self.current_volume)
        return {"message": f"Volume decreased to {self.current_volume}"}

    def stop_song(self):
        try:
            mixer.music.stop()
            return {"message": "Music stopped"}
        except Exception:
            raise Exception("Error stopping song")
