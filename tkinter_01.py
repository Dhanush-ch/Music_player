import os
from tkinter import *  # Tkinter Framework
import tkinter.messagebox  # To display types of message dialogBoxes
from mutagen.mp3 import MP3
import time
import threading
from tkinter import filedialog  # To browse files
from pygame import mixer  # To play the music

root = Tk()  # creating up the simple window

mixer.init()  # initializing the mixer

root.title("PyMusic")
# root.iconbitmap(r'PyMusic.ico')
# r - raw string or simply its asking for the location, iconbitmap()- To change the icon (In .ico format)

# GUI LAYOUTS- Pack & Grid

# StatusBar_Label
statusbar = Label(root, text="Welcome to PyMusic!", relief=GROOVE, anchor=W)
# anchor - Used to stick the text in some specific direction, W stands for West direction
statusbar.pack(side=BOTTOM, fill=X)  # X- x-axis

# Frames
left_frame = Frame(root)
left_frame.pack(side=LEFT, pady=10)

right_frame = Frame(root)
right_frame.pack()

mid_frame = Frame(right_frame)  # Frame- Used to frame or group the elements from a specific region into one frame
mid_frame.pack(pady=10)

top_frame = Frame(right_frame)
top_frame.pack()

bottom_frame = Frame(right_frame)
bottom_frame.pack()

# MenuBar
menubar = Menu(root)
root.config(menu=menubar)


# config()- To make sure menu bar sticks to the top, To ensure the menubar is ready to recieve sub-menus




# SubMenu
subMenu = Menu(menubar, tearoff=0)

playlist = []

# Open
def browse():
    global filename_path  # global - globalizes the variable
    filename_path = filedialog.askopenfilename()  # askopenfle()- inbuild function to ask and choose the file to open
    add_to_playlist(filename_path)

# playlist - Contains the full path + filename
# playlistbox - Contains only thr filename
# fullpath - filename is required to play the music inside the play_music load function


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)  # add_cascade()- Used to add sub-menus in menu bar
subMenu.add_command(label="Open", command=browse)  # add_command- Used to add cascade/dropdown menu in sub-menu
subMenu.add_command(label="Exit", command=root.destroy)  # destroy- Exits the window


# Help
def about_us():
    tkinter.messagebox.showinfo("About PyMusic", "This is a music player built using python by @DHANUSH")


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(labe="Help", menu=subMenu)
subMenu.add_command(label="About", command=about_us)  # A function should be declared above before calling it

# Images
play_img = PhotoImage(file="play_butt.png")
stop_img = PhotoImage(file="stop_butt.png")
pause_img = PhotoImage(file="pause_butt.png")
rewind_img = PhotoImage(file="backward.png")
mute_img = PhotoImage(file="mute.png")
vol_img = PhotoImage(file="volume.png")
fast_for = PhotoImage(file = "forward.png")

def show_details():
    text['text'] = "playing" + '-' + os.path.basename(filename_path)
    file_data = os.path.splitext(filename_path)

    if file_data[1] == '.mp3':
        audio = MP3(filename_path)
        total_length = audio.info.length
    else:
        # div - total_length/60, mod - total_length % 60
        a = mixer.Sound(filename_path)
        total_length = a.get_length()

    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length_label['text'] = "Total length " + '- ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy() - returns FALSE when we press the stop button (music stops playing)
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentlengthlabel['text'] = "Current time " + '- ' + timeformat
            time.sleep(1)
            t -= 1


def play_button():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = 'playing' + "- " + os.path.basename(filename_path)
        paused = FALSE
    else:
        try:
            mixer.music.load(filename_path)
            mixer.music.play()
            statusbar['text'] = 'Playing' + "- " + os.path.basename(filename_path)
            # os.path.basename- To show only the file name by hiding its location
            show_details()
        except:
            tkinter.messagebox.showerror("File not found!", "Error! could not find the file. Check again.")


def stop_button():
    mixer.music.stop()
    statusbar['text'] = "Music stopped."


paused = FALSE


def pause_butt():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Paused"


def set_vol(val):
    # val- inbuilt variable, in this case used to set the current volume number to this var
    volume = int(val) / 100
    mixer.music.set_volume(volume)  # set_volume- inbuilt function of mixer takes value only from 0 to 1


def rewind_butt():
    mixer.music.rewind()
    statusbar['text'] = "Music rewinded"


muted = FALSE


def mute_button():
    global muted
    global volume
    if muted:  # Unmute the music
        mixer.music.set_volume(0.5)
        vol_butt.configure(image=vol_img)
        scale.set(50)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        vol_butt.configure(image=mute_img)
        scale.set(0)
        muted = TRUE


def on_closing():
    stop_button()
    root.destroy()


# Labels

playlistbox = Listbox(left_frame)
playlistbox.pack()

length_label = Label(top_frame, text="Total length : --:--")
length_label.pack(pady=10)

currentlengthlabel = Label(top_frame, text="Current length : --:--", relief=GROOVE)
currentlengthlabel.pack(pady=10)

add_song = Button(left_frame, text="Add", command=browse)
add_song.pack(side=LEFT)

del_song = Button(left_frame, text="Del")
del_song.pack()

text = Label(top_frame, text="Lets make some noise!")
text.pack()

# Pause Button
pause_butt = Button(mid_frame, image=pause_img, command=pause_butt, borderwidth=0)
pause_butt.grid(row=0, column=0, padx=30)
# pady(padding Y-axis)- padding is technique used to add some space between the elements

# Rewind Button
rewind_butt = Button(mid_frame, image=rewind_img, command=rewind_butt, borderwidth=0)
rewind_butt.grid(row=0, column=1, padx=15)

# play Button
play_butt = Button(mid_frame, image=play_img, command=play_button, borderwidth=0)  # Button- converts img to button
play_butt.grid(row=0, column=2, padx=30)

'''# fast_forward
forward_butt = Button(mid_frame, image=fast_for, borderwidth= 0)  # Button- converts img to button
forward_butt.grid(row=0, column=3, padx=15) '''

# Stop Button
stop_butt = Button(mid_frame, image=stop_img, command=stop_button, borderwidth=0)  # Button()- To add a button
stop_butt.grid(row=0, column=4, padx=30)

# Mute Button
vol_butt = Button(bottom_frame, image=vol_img, command=mute_button, borderwidth=0)
vol_butt.grid(row=1, column=0)

# Scale button
scale = Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)  # Scale() - adds volume controller
scale.set(50)  # set() - sets the given value as default
mixer.music.set_volume(0.5)
scale.grid(row=1, column=1, padx=10)

# protocol - A way of communication
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
