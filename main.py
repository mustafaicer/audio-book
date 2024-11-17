import customtkinter as ctk
from PIL import Image
import pygame
import threading
import gtts
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.desktop = os.path.expanduser("~\\Desktop")
        self.audio_book_folder = os.path.join(self.desktop, "Audio Book")
        try:
            os.mkdir(self.audio_book_folder)
        except:
            pass

        self.title("Audio Book")
        self.iconbitmap("images/icon.ico")
        self.minsize(width=900,height=600)
        self.maxsize(width=900,height=600)
        self.configure(padx=10,pady=10)


        self.choose_lang = None
        self.textbox = None
        self.audio_file_path = None
        self.audio_file = None
        self.file_name = None
        self.audio_lang = None
        self.text = None

        self.info_label = ctk.CTkLabel(self,font=('Arial',18,'bold'))
        self.ui()

    def ui(self):
        convert_audio_button = ctk.CTkButton(self,text="Convert text to audio",width=200,font=('Arial',16,'bold'),command=self.convert_audio)
        convert_audio_button.place(relx=0.01,rely=0.01)

        self.choose_lang = ctk.CTkComboBox(self,values=["Türkçe", "English"])
        self.choose_lang.place(relx=0.25,rely=0.01)

        play_icon = ctk.CTkImage(dark_image=Image.open("images/play.png"),size=(20,20))
        play_icon_button = ctk.CTkButton(self,text="",image=play_icon,width=40,fg_color="transparent",hover=False,command=play_audio)
        play_icon_button.place(relx=0.425,rely=0.01)

        pause_icon = ctk.CTkImage(dark_image=Image.open("images/pause.png"), size=(20, 20))
        pause_icon_button = ctk.CTkButton(self, text="", image=pause_icon, width=40,fg_color="transparent",hover=False,command=pause_audio)
        pause_icon_button.place(relx=0.475, rely=0.01)

        restart_icon = ctk.CTkImage(dark_image=Image.open("images/restart.png"), size=(20, 20))
        restart_icon_button = ctk.CTkButton(self, text="", image=restart_icon, width=40,fg_color="transparent",hover=False,command=restart_audio)
        restart_icon_button.place(relx=0.525, rely=0.01)

        self.textbox = ctk.CTkTextbox(self,width=860,height=500,padx=10,pady=10,font=('Arial',16,'normal'))
        self.textbox.place(relx=0.01,rely=0.1)

    def convert_audio(self):
        file_name_input = ctk.CTkInputDialog(title="File Name Input",text="Enter Audio File Name ")
        self.file_name = file_name_input.get_input()

        self.audio_lang = self.choose_lang.get()
        self.text = self.textbox.get(1.0,ctk.END)

        thread = threading.Thread(target=self.start_create_audio)
        self.info_label.configure(text="Wait",text_color="light yellow")
        self.info_label.place(relx=0.575,rely=0.01)
        thread.start()

    def start_create_audio(self):
        if self.audio_lang == "English":
            self.audio_file = gtts.gTTS(text=self.text,lang='en')
        elif self.audio_lang == "Türkçe":
            self.audio_file = gtts.gTTS(text=self.text, lang='tr')
        self.audio_file_path = os.path.join(self.audio_book_folder, self.file_name)
        self.audio_file.save(f"{self.audio_file_path}.mp3")
        pygame.mixer.music.load(f"{self.audio_file_path}.mp3")
        self.info_label.configure(text="")
        self.info_label.configure(text="Done",text_color="light green")
        self.info_label.place(relx=0.575,rely=0.01)

        pygame.mixer.music.play()
        pygame.mixer.music.pause()

def play_audio():
    pygame.mixer.music.unpause()

def pause_audio():
    pygame.mixer.music.pause()

def restart_audio():
    pygame.mixer.music.play()

if __name__ == "__main__":
    window = App()
    window.mainloop()