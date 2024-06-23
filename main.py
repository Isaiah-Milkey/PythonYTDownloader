import tkinter
import customtkinter
from pytube import YouTube

# Tutorial closely followed and edited from @developedbyed on YouTube
# Link: https://www.youtube.com/watch?v=NI9LXzo0UY0

def start_download():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        if(switch.get() != "on"):
            print("getting video!")
            print(dropdown.get())
            # video = ytObject.streams.filter(res=resolution, only_audio=False).first()
            # video = ytObject.streams.get_by_resolution(res=resolution)
            try:
                # video = ytObject.streams.get_by_resolution(res=dropdown.get())
                video = ytObject.streams.filter(res=dropdown.get(),abr="320kbps", bitrate="320kbps").order_by('resolution').desc().first()
                video.download()
                # print("finished resolutiuon download!!")
            except:
                video = ytObject.streams.get_highest_resolution()
                video.download()
                # print("entered except download!")
        else:
            print("audio only!")
            video = ytObject.streams.get_audio_only()
            video.download()
    except:
        print("Youtube link is invalid")
    print("Download Complete")

def toggle_audio():
    pass

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = bytes_downloaded / total_size * 100
    per = str(int(percentage_completed))
    #update percentage
    percent_val.configure(text=per + '%')
    percent_val.update()

    #update progress bar
    progressbar.set(float(percentage_completed) / 100)
        
# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Our app frame
app = customtkinter.CTk()
width = 720
height = 480
window_size = str(width) + "x" + str(height)
app.geometry(window_size)
app.title("Youtube Downloader")

# Adding UI Elements
title = customtkinter.CTkLabel(app, text="Insert a YouTube link")
title.pack(padx=10, pady=10)

# Link Input
url_var=tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(padx=(width/5,0), pady=10, side=tkinter.LEFT)

# Download Button
download = customtkinter.CTkButton(app, text="Download", command=start_download)
download.pack(padx=(3, width/5), pady=10, side=tkinter.LEFT)

# Dropdown Box
dropdown = customtkinter.CTkOptionMenu(app, values = [
"144p", "240p", "360p", "480p", "720p"
])
dropdown.place(x=width/5, y=height/1.5)
resolution = dropdown.get()

# Audio Toggle
switch_val = customtkinter.StringVar(value="on")
switch = customtkinter.CTkSwitch(app, text="Audio Only", command=toggle_audio, variable=switch_val, onvalue="on", offvalue="off")
switch.place(x=width/2, y=height/1.5)

# Progress Percentage
percent_val = customtkinter.CTkLabel(app, text="0%")
percent_val.place(x=width/3.5, y=height/1.23)

progressbar = customtkinter.CTkProgressBar(app )
progressbar.set(0)
progressbar.place(x=width/3, y=height/1.2)

# Run app continually
app.mainloop()