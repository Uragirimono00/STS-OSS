import time
from tkinter import *
from pynput.keyboard import Controller
import os
import threading
import speech_recognition as sr
from gtts import gTTS
import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

type = 'Naver'

base_url = 'https://papago.naver.com'
chrome_options = Options()  # 브라우저 꺼짐 방지
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # 불필요한 에러 메세지 삭제
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-san블랙팬서는 와칸다 아무튼 그리고 정신감정을 받던 중 갑자기 갑자기 dbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.set_window_size(1920, 1080)
driver.implicitly_wait(10)

driver.get(base_url)

class voiceloop(threading.Thread):
    mykeyboard = Controller()
    def run(self) -> None:

        while True:
            voice = self.CollectVoice()
            if voice != False and myThread.rflag == True:
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
                print("조정중...")

                # 설정
                listener.adjust_for_ambient_noise(raw_voice, 2)
                listener.dynamic_energy_adjustment_damping = 0.2
                listener.pause_threshold = 0.8
                listener.energy_threshold = 600

                img_frm.config(image=mic1_img)

                print("듣고 있습니다...")
                audio = listener.listen(raw_voice)

                img_frm.config(image=mic2_img)

                voice_data = listener.recognize_google(audio, language='ko')

            except UnboundLocalError:
                pass

            except sr.UnknownValueError:
                print("이해할 수 없습니다.")
                return False

            return str(voice_data)


def on_closing():
    myThread.rflag = False
    print("종료되었습니다.")
    # myThread.join()
    os._exit(1)

def speak(text):
    if type == "Google":
        tts = gTTS(text=text, lang='ko')
        file_name = 'voice.mp3'
        tts.save(file_name)
        if os.path.exists(file_name):
            try:
                playsound.playsound(file_name)
                os.remove(file_name)
            except:
                print("에러가 발생했습니다.")
                pass
        return
    if type == "Naver":
        driver.find_element(By.XPATH, '//*[@id="txtSource"]').click()
        driver.find_element(By.ID, "txtSource").clear()
        driver.find_element(By.ID, "txtSource").send_keys(text)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@class="btn_sound___2H-0Z"]').click()
        time.sleep(3)
        return
    else:
        print("타입 설정이 이상합니다.")
        return

root = Tk()
root.title("STS")
root.geometry("200x200+50+50")

mic1_img = PhotoImage(file="mic1.png")
mic2_img = PhotoImage(file="mic2.png")
mic3_img = PhotoImage(file="mic3.png")

img_frm = Label(root, image=mic2_img)
img_frm.pack()

myThread = voiceloop()
myThread.rflag = True
myThread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.wm_attributes("-topmost", 1)
root.mainloop()
