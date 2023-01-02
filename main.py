from tkinter import *
from pynput.keyboard import Controller
import os
import threading
import speech_recognition as sr
from gtts import gTTS
import playsound


class voiceloop(threading.Thread):
    mykeyboard = Controller()

    def run(self) -> None:

        while True:
            voice = self.CollectVoice()

            if voice != False and myThread.rflag == True:
                print(voice)
                speak(voice)
                self.Pasting(voice)

            if myThread.rflag == False:
                break

    def Pasting(self, myvoice):
        for character in myvoice:
            self.mykeyboard.type(character)
        self.mykeyboard.type(" ")

    def CollectVoice(self):
        # get microphone device on notebook or desk top
        listener = sr.Recognizer()
        voice_data = ""

        with sr.Microphone() as raw_voice:

            try:
                img_frm.config(image=mic3_img)
                print("Adjusting")
                listener.adjust_for_ambient_noise(raw_voice)

                # adjust setting values
                listener.dynamic_energy_adjustment_damping = 0.15
                listener.pause_threshold = 0.6
                listener.energy_threshold = 600

                img_frm.config(image=mic1_img)

                print("Say something!")
                audio = listener.listen(raw_voice, 10, 5)

                img_frm.config(image=mic2_img)

                voice_data = listener.recognize_google(audio, language='ko')

            except UnboundLocalError:
                pass

            except sr.UnknownValueError:
                print("could not understand audio")
                return False

            return str(voice_data)


def on_closing():
    myThread.rflag = False
    print("finish work")
    # myThread.join()
    os._exit(1)


def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = './voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    if os.path.exists(filename):
        os.remove(filename)


root = Tk()
root.title("Voice Collector")
root.geometry("200x200+50+50")

mic1_img = PhotoImage(file="mic1.png")
mic2_img = PhotoImage(file="mic2.png")
mic3_img = PhotoImage(file="mic3.png")

img_frm = Label(root, image=mic2_img)
img_frm.pack();

myThread = voiceloop()
myThread.rflag = True
myThread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.wm_attributes("-topmost", 1)
root.mainloop()
