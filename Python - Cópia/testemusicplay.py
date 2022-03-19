from tkinter.constants import END, RAISED, SOLID, SUNKEN
from pygame import mixer
from tkinter import Listbox, PhotoImage, Tk
from tkinter import Label
from tkinter import Button
from tkinter import filedialog

current_volume = float(0.5)
#Functions
def play_song():
    filename = filedialog.askopenfilename(initialdir = "C:/Python/Playlist/", title = "Please select a file", filetypes=(("Mp3 Files", "*.mp3"),))
    #Playlist_box.insert(END,filename)
    current_song = filename
    song_title = filename.split("/")
    song_title = song_title[-1]
    Playlist_box.insert(END,song_title)
            

    try:
        mixer.init()
        mixer.music.load(current_song)
        mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(fg ="green", text ="Now playing : " + str(song_title))
        volume_label.config(fg="green", text = "volume : " + str(current_volume))

    except Exception as e:
        print(e)
        song_title_label.config(fg= "red",  text = "Error playing track")
def reduce_volume():
    try:
        global current_volume
        if current_volume <= 0:
            volume_label.config(fg="red", text = "Volume = Muted")
            return
        current_volume = current_volume - float(0.1)
        current_volume = round(current_volume,1)
        mixer.music.set_volume(current_volume)
        volume_label.config(fg = "green", text = "Volume : "+str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg = "red", text = "Track hasn't been selected yet")


def increase_volume():
    try:
        global current_volume
        if current_volume >=1 :
            volume_label.config(fg="green", text = "Volume = Max")
            return
        current_volume = current_volume + float(0.1)
        current_volume = round(current_volume,1)
        mixer.music.set_volume(current_volume)
        volume_label.config(fg = "green", text = "Volume : "+str(current_volume))
    except Exception as e:
        print(e)
        song_title_label.config(fg = "red", text = "Track hasn't been selected yet")


def pause():
    try:
        mixer.music.pause()
    except Exception as e:
        print(e)
        song_title_label.config(fg = "red", text = "Track hasn't been selected yet")


def resume():
    try:
       mixer.music.unpause()
    except Exception as e:
        print(e)
        song_title_label.config(fg = "red", text = "Track hasn't been selected yet")

def previous():
    pass

def next():
    pass

def add_song_playlist():
    pass

#Mainscreen
master = Tk()
#master.wm_maxsize(410, 175)
master.title("music player")


#Labels
label_1 = Label(master,
      text = "Custom Music Player",
      font = "Calibri 15",
      bg= "black",
      bd=5,
      relief= RAISED,
      fg = "red",).grid(sticky="N", row=0)

label_2 = Label(master,
      text = "Please select a music track you would like to play",
      font = "Calibri 12",
       width = 50,
       fg = "blue").grid(sticky="N", row=1)
label_3 = Label(master,
      text = "Volume",
      width = 12,
      font = "Calibri 12",
      bg= "black",
      bd=5,
      relief= SUNKEN,
      fg = "red",).grid(sticky="N", row=5)

song_title_label = Label(master,
                font = "Calibri")
song_title_label.grid(stick="N", row=4)
volume_label = Label(master,
                     font = "Calibri, 12")
volume_label.grid(sticky="N", row=7, pady=5)
Playlist_box = Listbox(master, bg="black", fg="green", width=50)
Playlist_box.grid(row=2, sticky = "N")
#Playlist_box.grid_forget()

play_button_img = PhotoImage(file='C:/Users/User/Documents/Python/imagens/play-button.png')
select_song_img = PhotoImage(file='C:/Users/User/Documents/Python/imagens/playlist.png')
pause_button_img = PhotoImage(file='C:/Users/User/Documents/Python/imagens/pause.png')
volume_reduce_button_img = PhotoImage(file='C:/Users/User/Documents/Python/imagens/reduce-volume.png')
volume_increase_button_img = PhotoImage(file='C:/Users/User/Documents/Python/imagens/increase-volume.png')


#Buttons
Button(master, image= select_song_img, borderwidth=0 , font = "Calibri 12" , command = play_song).grid(row=3, sticky = "N")
Button(master, image= pause_button_img, borderwidth=0, font="Calibri,12", command = pause).grid(row=5, sticky="E")
Button(master, image= play_button_img, borderwidth=0, font="Calibri,12", command = resume).grid(row=5, sticky="W")
Button(master, image= volume_reduce_button_img, borderwidth=0, font="Calibri,12", command = reduce_volume).grid(row=7, sticky="W")
Button(master, image= volume_increase_button_img,borderwidth=0, font="Calibri,12", command = increase_volume).grid(row=7, sticky="E")
master.mainloop()
