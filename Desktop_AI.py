import os
import subprocess
import speech_recognition as sr
import pyttsx3
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep

# Initialize the speech engine
engine = pyttsx3.init()

# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-in')
        print(f"Command: {command}\n")
    except Exception as e:
        print("Could not understand audio, please try again.")
        return None
    return command.lower()

# Function to open files based on the file path
def open_file(file_path):
    try:
        os.startfile(file_path)  # Windows
    except AttributeError:
        subprocess.call(["open", file_path])  # Mac
    except Exception as e:
        speak(f"Sorry, I couldn't open {file_path}. {e}")

# Function to open applications
def open_application(app_name):
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(app_name)
        elif os.name == 'posix':  # Mac/Linux
            subprocess.call(["open", "-a", app_name])
        speak(f"{app_name} is opening")
    except Exception as e:
        speak(f"Sorry, I couldn't open {app_name}. {e}")

# Function to open websites
def open_website(website_url):
    try:
        webbrowser.open(website_url)
        speak(f"Opening {website_url}")
    except Exception as e:
        speak(f"Sorry, I couldn't open the website {website_url}. {e}")

# Function to send an email
def send_email(to_address, subject, body):
    try:
        sender_email = "your_email@example.com"
        sender_password = "your_password"  # Use environment variables for better security
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_address
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_address, text)
        server.quit()

        speak("Email sent successfully")
    except Exception as e:
        speak(f"Sorry, I couldn't send the email. {e}")

# Function to shut down the PC
def shut_down_pc():
    try:
        speak("Shutting down the system in 10 seconds. Save your work.")
        sleep(10)
        if os.name == 'nt':  # Windows
            os.system('shutdown /s /t 1')
        elif os.name == 'posix':  # Mac/Linux
            os.system('shutdown now')
    except Exception as e:
        speak(f"Sorry, I couldn't shut down the system. {e}")

# Function to restart the PC
def restart_pc():
    try:
        speak("Restarting the system.")
        if os.name == 'nt':  # Windows
            os.system('shutdown /r /t 1')
        elif os.name == 'posix':  # Mac/Linux
            os.system('shutdown -r now')
    except Exception as e:
        speak(f"Sorry, I couldn't restart the system. {e}")

# Function to handle user commands
def handle_command(command):
    if 'open file' in command:
        speak("Please provide the file path.")
        file_path = input("File Path: ")
        open_file(file_path)

    elif 'open application' in command:
        speak("Please provide the application name.")
        app_name = input("Application Name: ")
        open_application(app_name)

    elif 'open website' in command:
        speak("Please provide the website URL.")
        website_url = input("Website URL: ")
        open_website(website_url)

    elif 'send email' in command:
        speak("Please provide the recipient's email address.")
        to_address = input("Recipient Email: ")
        speak("What should be the subject?")
        subject = input("Email Subject: ")
        speak("What is the message?")
        body = input("Email Body: ")
        send_email(to_address, subject, body)

    elif 'shut down' in command:
        shut_down_pc()

    elif 'restart' in command:
        restart_pc()

    elif 'exit' in command or 'quit' in command:
        speak("Goodbye!")
        return False

    else:
        speak("Sorry, I didn't understand that command.")

    return True

# Main Assistant function
def assistant():
    speak("Hello, how can I assist you today?")
    active = True
    while active:
        command = listen()
        if command:
            active = handle_command(command)

# Run the assistant
if __name__ == "__main__":
    assistant()
