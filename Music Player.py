import os
import pickle 
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        mixer.init()

        if os.path.exists('songs.pickle'):
            with open('songs.pickle', 'rb') as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        self.current = 0
        self.paused = True
        self.played = False

        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()

    def create_frames(self):
        self.track = tk.LabelFrame(self, text='Song Track',
                                   font=("times new romen",15,"bold"),
                                   bg="grey",fg="black",bd=5,relief=tk.GROOVE)
        self.track.configure(width=410, height=300)
        self.track.grid(row=0,column=0)

        self.tracklist = tk.LabelFrame(self, text=f'Playlist - {len(self.playlist)}',
                                   font=("times new romen",15,"bold"),
                                   bg="grey",fg="black",bd=5,relief=tk.GROOVE)
        self.tracklist.configure(width=190, height=400)
        self.tracklist.grid(row=0,column=1, rowspan=3, pady=5)
    
        self.controls = tk.LabelFrame(self,font=("times new romen",15,"bold"),
                                   bg="grey",fg="white",bd=2,relief=tk.GROOVE)
        self.controls.configure(width=410, height=80)
        self.controls.grid(row=2,column=0, pady=5,padx=10)

    def track_widgets(self):
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=400, height = 240)
        self.canvas.grid(row=0,column=0)

        self.songtrack = tk.Label(self.track, font=("times new romen",15,"bold"),
                               bg="white", fg="dark blue")
        self.songtrack['text'] = 'Music Player MP3'
        self.songtrack.configure(width=30, height = 1)
        self.songtrack.grid(row=1,column=0)

    def control_widgets(self):
        self.loadSongs = tk.Button(self.controls, bg="green", fg="white", font=10)
        self.loadSongs['text'] = "Load Songs"
        self.loadSongs['command'] = self.retrive_songs
        self.loadSongs.grid(row=0,column=0, padx=10)

        self.prev = tk.Button(self.controls, image=prev,bg='white')
        self.prev['command'] = self.prev_song
        self.prev.grid(row=0,column=1, padx=2, pady=7)

        self.pause = tk.Button(self.controls, image=pause,bg='white')
        self.pause['command'] = self.pause_song
        self.pause.grid(row=0,column=2, padx=2, pady=7)

        self.next_ = tk.Button(self.controls, image=next_,bg='white')
        self.next_['command'] = self.next_song
        self.next_.grid(row=0,column=3, padx=2, pady=7)

        self.volume = tk.DoubleVar()
        self.slider = tk.Scale(self.controls, from_= 0, to=100, orient=tk.HORIZONTAL)
        self.slider['variable'] = self.volume
        self.slider.set(40)
        mixer.music.set_volume(4.0)
        self.slider['command'] = self.change_volume
        self.slider.grid(row=0,column=4,padx=5)


    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0,column=1,rowspan=5,sticky='ns')

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                               yscrollcommand=self.scrollbar.set, selectbackground="sky blue")
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind('<Double-1>', self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)



    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    def retrive_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root_, dirs , files in os.walk(directory):
            print(dirs)
            for file in files:
                if os.path.splitext(file)[1] == '.mp3':
                    path = (root_ + '/' + file).replace('\\','/')
                    self.songlist.append(path)

        with open('songs.pickle', 'wb') as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist['text'] = f'Playlist - {str(len(self.playlist))}'
        self.list.delete(0, tk.END)
        self.enumerate_songs()
    
    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg='white')

        mixer.music.load(self.playlist[self.current])

        self.pause['image'] = pause
        self.paused = False
        self.play = True
        self.songtrack['anchor'] = 'w'
        self.songtrack['text'] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg='sky blue')
        mixer.music.play()

    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause['image'] = play
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause['image'] = pause

    def prev_song(self):
        if self.current > 0:
            self.current -=1
        else:
            self.current = 0
        self.list.itemconfig(self.current+1, bg='white')
        self.play_song()

    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current +=1
        else:
            self.current = 0
            self.play_song()
        self.list.itemconfig(self.current-1, bg='white')
        self.play_song()

    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 100)

root = tk.Tk()
root.geometry('650x410')
root.resizable(False,False)
root.wm_title('Music Player')
root.config(bg='wheat')
root.iconbitmap('title icon.ico')

img = PhotoImage(file='maker.gif')
prev = PhotoImage(file='prev2.png')
next_ = PhotoImage(file='next2.png')
pause = PhotoImage(file='pause2.png')
play = PhotoImage(file='play2.png')

app = Player(master=root)
app.mainloop()