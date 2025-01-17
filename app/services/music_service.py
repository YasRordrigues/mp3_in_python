import os
from pygame import mixer

class MusicService:
    def __init__(self):
        self.current_song = None
        self.is_paused = False
        self.current_volume = 0.5
        mixer.init()

    def play_song(self, file_path):
        if self.current_song == file_path and self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            return {"message": "Resumed song"}
        else:
            self.stop_song()
            mixer.music.load(file_path)
            mixer.music.set_volume(self.current_volume)
            mixer.music.play()
            self.current_song = file_path
            self.is_paused = False
            return {"message": f"Playing {os.path.basename(file_path)}"}

    def pause_song(self):
        mixer.music.pause()
        self.is_paused = True
        return {"message": "Song paused"}

    def resume_song(self):
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            return {"message": "Song resumed"}
        else:
            raise Exception("No song to resume")

    def stop_song(self):
        mixer.music.stop()
        self.is_paused = False
        self.current_song = None
        return {"message": "Song stopped"}
