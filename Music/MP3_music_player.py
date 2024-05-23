#importing libraries 
import pygame
from pygame import mixer
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
from tkinter import messagebox
#creating the root window 
root=Tk()
root.title('Music player App')
photo = PhotoImage(file = "icon2.png")
root.wm_iconphoto(False, photo)
root.geometry("800x600")
root.resizable(False, False)
#initialize mixer 
mixer.init()
#create the listbox to contain songs
songsframe=LabelFrame(root, text="Songs Playlist", bg="skyblue",fg="black", bd=5, relief=GROOVE)
songsframe.place(x=0, y=0, width=800, height=400)
songs_list=Listbox(songsframe,selectmode=SINGLE,bg="white",fg="black",font=('arial',15),height=15,width=70,selectbackground="#70f49f",selectforeground="black")
songs_list.grid(columnspan=10)
#control frams
buttonFrame= LabelFrame(root, text="Control Pannel", font=("times new roman",15, "bold"), bg="#f4ae70",fg="white", bd=5, relief=GROOVE)
buttonFrame.place(x=0, y=460, width=800, height=100)
def Play():
    selected_index = songs_list.curselection()
    if selected_index:
        selected_path = song_paths[selected_index[0]]
        mixer.music.load(selected_path)
        mixer.music.play()
        # Call the plytime function to update play time
        play_time()
        update_time_and_slider()
  
#play button
clickplay=PhotoImage(file="play.png")
play_label= Label(image=clickplay)
play_button=Button(buttonFrame,image=clickplay,width =50,command=Play)
play_button.grid(row=1,column=0)

music_total_length=300 #Length of music
# grab song lenght time info
def play_time():
    # This is to get the song length in seconds
    current_time = pygame.mixer.music.get_pos() / 1000
    # This is to convert the above seconds into a time format
    converted_current_time = time.strftime('%H:%M:%S', time.gmtime(current_time))
    # This is to update time every second
    status_bar.after(1000, play_time)
    # Get currently playing song
    selected_index = songs_list.curselection()
    if selected_index:
        selected_path = song_paths[selected_index[0]]
        song_length = MP3(selected_path).info.length
        converted_song_length = time.strftime('%H:%M:%S', time.gmtime(song_length))
        # This is to display
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        # If the song finishes, call the Next() function
        if int(current_time) >= int(song_length):
            Next()
#to pause the song 
def Pause():
    mixer.music.pause()
#pause button 
clickpause=PhotoImage(file="pause.png")
pause_label= Label(image=clickpause)
pause_button=Button(buttonFrame,image=clickpause,width =50,command=Pause)
pause_button.grid(row=1,column=2)
#to stop the  song 
def Stop():
    mixer.music.stop()
    songs_list.selection_clear(0, END)  # Clear selection from the listbox
    status_bar.config(text="") 
#stop button
clickstop=PhotoImage(file="stop.png")
stop_label= Label(image=clickstop)
stop_button=Button(buttonFrame,image=clickstop,width =50,command=Stop)
stop_button.grid(row=1,column=1)
#to resume the song
def Resume():
    mixer.music.unpause()
#resume button
clickresume=PhotoImage(file="resume.png")
resume_label= Label(image=clickresume)
Resume_button=Button(buttonFrame,image=clickresume,width =50,command=Resume)
Resume_button.grid(row=1,column=3)
#Function to navigate from the current song
def Previous():
    # Get the index of the currently selected song
    selected_index = songs_list.curselection()
    if selected_index:
        # Get the index of the previous song
        previous_index = selected_index[0] - 1
        # If previous_index is negative, set it to the last song index
        if previous_index < 0:
            previous_index = songs_list.size() - 1
        # Get the path of the previous song
        previous_path = song_paths[previous_index]
        # Load and play the previous song
        mixer.music.load(previous_path)
        mixer.music.play()
        # Clear the selection in the listbox
        songs_list.selection_clear(0, END)
        # Activate and select the previous song in the listbox
        songs_list.activate(previous_index)
        songs_list.selection_set(previous_index)
#previous button
clickprevious=PhotoImage(file="previous.png")
previous_lable=Label(image=clickprevious)
previous_button=Button(buttonFrame,image=clickprevious,width =50,command=Previous)
previous_button.grid(row=1,column=4)
def Next():
    # Get the index of the currently selected song
    selected_index = songs_list.curselection()
    if selected_index:
        # Get the index of the next song
        next_index = selected_index[0] + 1
        # If next_index is greater than or equal to the number of songs, set it to 0
        if next_index >= songs_list.size():
            next_index = 0
        # Get the path of the next song
        next_path = song_paths[next_index]
        # Load and play the next song
        mixer.music.load(next_path)
        mixer.music.play()
        # Clear the selection in the listbox
        songs_list.selection_clear(0,END)
        # Activate and select the next song in the listbox
        songs_list.activate(next_index)
        songs_list.selection_set(next_index)
#nextbutton
clicknext=PhotoImage(file="next.png")
next_label=Label(image=clicknext)
next_button=Button(buttonFrame,image=clicknext,width =50,command=Next)
next_button.grid(row=1,column=5)
#volume function
def VolAdj(VOLUME):
    mixer.music.set_volume(VolumeSlider.get()/100)
#Volume = slider
import tkinter 
VolumeSlider=tkinter.Scale(buttonFrame,from_= 0,to=100,length = 200, label='Volume Control', orient = 'horizontal', fg = 'black', bg='light blue',command=VolAdj)
VolumeSlider.set(15)
VolumeSlider.grid(row=1,column=6)


#status bar
status_bar=LabelFrame(root, text="00:00",bd=1, relief=GROOVE)
status_bar.place(x=0,y=400, width=800, height=20) 

def update_time_and_slider():
    # Get the current time of the music in seconds
    current_time = pygame.mixer.music.get_pos() / 1000
    LengthSlider.config(to=int(music_total_length))
    LengthSlider.config(state='normal')
    LengthSlider.set(current_time)
    LengthSlider.config(state='disabled')
    # Call itself after 1 second
    root.after(1000, update_time_and_slider)

LengthSlider=tkinter.Scale(root,from_=0, to=int(music_total_length), 
    orient = 'horizontal', fg = 'black', bg='light blue',showvalue=0)
LengthSlider.place(x=0, y=420, width=800, height=40)
LengthSlider.config(state='disabled')
# LengthSlider.bind("<Motion>",update_time_and_slider)

#menu 
my_menu=Menu(root)
root.config(menu=my_menu)
add_song_menu=Menu(my_menu)
about=Menu(my_menu)
my_menu.add_cascade(label="Menu",menu=add_song_menu)
my_menu.add_cascade(label="Help",menu=about)
#add many songs to the playlist of python mp3 player
def about_developer():
    messagebox.showinfo("Developer", "Nitesh Kumar\nhttps://www.linkedin.com/in/nitishsangwan/")
def about_app():
    messagebox.showinfo("Music Player -v 1.0.0", "Music player Application developed in Python")


about.add_command(label="About",command=about_app)
about.add_command(label="Developer",command=about_developer)

import os
def get_filename_from_path(file_path):
    return os.path.basename(file_path)
song_paths = []
def addsongs():
    #to open a file  
    temp_song=filedialog.askopenfilenames(initialdir="Music/",title="Choose a song", filetypes=(("mp3 Files","*.mp3"),("m4a Files","*.m4a")))
    ##loop through every item in the list to insert in the listbox
    for s in temp_song:
        song_paths.append(s)
        filename = get_filename_from_path(s)
        songs_list.insert(END, filename)
    # Play the first song automatically if the list is not empty
    if song_paths:
        mixer.music.load(song_paths[0])
        mixer.music.play()
        songs_list.selection_clear(0, END)
        songs_list.selection_set(0)
        play_time()
        update_time_and_slider()

add_song_menu.add_command(label="Add songs",command=addsongs)
def deletesong():
    curr_song=songs_list.curselection()
    songs_list.delete(curr_song[0])
add_song_menu.add_command(label="Delete song",command=deletesong)
mainloop()