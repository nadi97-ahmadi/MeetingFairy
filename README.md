# 🧸 Meeting Fairy

A cute desktop assistant that connects to Google Calendar and shows animated sticker notifications with custom audio alerts when your meetings are about to start.

---

##  Overview

Meeting Fairy is a lightweight background desktop application that helps you never miss a meeting again in a fun and aesthetic way. Instead of boring system notifications, it shows a floating animated sticker, plays a custom audio alert, and runs silently in the system tray while checking your Google Calendar automatically.

---

## 🎯 Features

📅 Google Calendar Integration  
Connects to your Google Calendar and detects upcoming meetings automatically in real time.

🧸 Animated Visual Notifications  
Shows a floating animated sticker across the screen with smooth movement and minimal UI design.

🔊 Custom Audio Alerts  
Plays your own voice or sound file (voice.mp3). No robotic system voice, fully customizable audio experience.

🖥 Background System Tray App  
Runs silently in the background with a system tray icon. Right-click options include Check Now, Test Popup, and Quit.

---

##  How It Works

The application runs in the background and continuously checks your Google Calendar for upcoming events. When a meeting is detected within the time window, it triggers a visual sticker animation on the screen and plays a custom audio alert. After the animation completes, everything closes automatically while the app continues running silently in the system tray.

---

## 📦 Installation

Clone the repository:

git clone https://github.com/nadi97-ahmadi/MeetingFairy.git  
cd MeetingFairy  

Create a virtual environment (recommended):

python -m venv venv  
venv\Scripts\activate  

Install dependencies:

pip install -r requirements.txt  

Add required files into the project folder:

credentials.json (Google Cloud OAuth file)  
sticker.png (animated sticker image)  
voice.mp3 (custom audio or voice file)  

---

## 🔐 Google Calendar Setup

To use Meeting Fairy, you must connect your Google account. First, go to Google Cloud Console and create a new project. Enable the Google Calendar API. Then create OAuth credentials for a Desktop App and download the credentials.json file. Place this file inside your project folder.

On first run, the application will open a browser window where you sign in with your Google account. After authorization, a token is saved locally so you do not need to log in again.

---

## ▶️ Run the App

Run the application using:

python main.py  

The app will start in the system tray and run silently in the background. It will automatically show animations when a meeting is detected.

---

## 📦 Build EXE (Windows)

To convert the project into a standalone desktop application, use PyInstaller:

pyinstaller --onefile --noconsole ^  
--add-data "credentials.json;." ^  
--add-data "sticker.png;." ^  
--add-data "voice.mp3;." ^  
main.py  

The final executable will be created in the dist folder as main.exe.

---

## 📁 Project Structure

MeetingFairy/  
main.py  
requirements.txt  
README.md  
sticker.png  
voice.mp3  
credentials.json  
venv/  

---

## ⚠️ Security Notice

Do not upload credentials.json, token.pickle, or venv to GitHub. These files are personal and must remain local on your machine. The .gitignore file ensures they are not pushed to the repository.

---

## 💡 Future Improvements

Future versions of Meeting Fairy may include AI-powered meeting summaries, multiple sticker themes, customizable sound packs, desktop widget mode, mobile companion app integration, and smart priority notifications.

---

## ❤️ About

Meeting Fairy was created as a fun and aesthetic productivity tool to make calendar reminders more engaging, visual, and enjoyable instead of boring system alerts.

- Made with love by Nadira -
