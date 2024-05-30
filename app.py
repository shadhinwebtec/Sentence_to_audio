import tkinter as tk
from tkinter import ttk, filedialog
from gtts import gTTS
from io import BytesIO
import tempfile
import pygame

temp_audio_path = None
is_paused = False

def convert_text_to_speech():
    global temp_audio_path
    text = text_entry.get("1.0", "end-1c")
    if text:
        tts = gTTS(text=text, lang="en", slow=False)
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_data.read())
            temp_audio_path = temp_audio.name

        enable_buttons()

def play_audio():
    global is_paused
    if temp_audio_path:
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_path)
        pygame.mixer.music.play()
        is_paused = False
        pause_button.config(state="normal")

def pause_audio():
    global is_paused
    if not is_paused:
        pygame.mixer.music.pause()
        pause_button.config(text="Resume")
    else:
        pygame.mixer.music.unpause()
        pause_button.config(text="Pause")
    is_paused = not is_paused

def download_audio():
    text = text_entry.get("1.0", "end-1c")
    if text:
        tts = gTTS(text=text, lang="en", slow=False)
        audio_data = BytesIO()
        tts.write_to_fp(audio_data)

        file_path = filedialog.asksaveasfilename(defaultextension=".mp3")
        if file_path:
            with open(file_path, "wb") as audio_file:
                audio_file.write(audio_data.getvalue())

def clear_text_box():
    global temp_audio_path, is_paused
    text_entry.delete("1.0", "end")
    temp_audio_path = None
    is_paused = False
    disable_buttons()
    pause_button.config(text="Pause", state="disabled")

def enable_buttons():
    play_button.config(state="normal")
    download_button.config(state="normal")

def disable_buttons():
    play_button.config(state="disabled")
    download_button.config(state="disabled")
    pause_button.config(state="disabled")

root = tk.Tk()
root.title("Text-to-Speech Converter")

text_entry = tk.Text(root, height=20, width=100)
text_entry.pack(pady=10)

convert_button = ttk.Button(root, text="Convert to Speech", command=convert_text_to_speech)
convert_button.pack(pady=5)

play_button = ttk.Button(root, text="Play", command=play_audio, state="disabled")
play_button.pack(pady=5)

pause_button = ttk.Button(root, text="Pause", command=pause_audio, state="disabled")
pause_button.pack(pady=5)

download_button = ttk.Button(root, text="Download Audio", command=download_audio, state="disabled")
download_button.pack(pady=5)

clear_button = ttk.Button(root, text="Clear", command=clear_text_box)
clear_button.pack(pady=5)

disable_buttons()

root.mainloop()
