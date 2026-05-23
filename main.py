import tkinter as tk
import threading
import schedule
import time
import datetime
import pickle
import os
import random
import sys
import pystray
from PIL import Image, ImageDraw, ImageTk
from playsound import playsound
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ---------------- CONFIG ----------------

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
notified = set()

MESSAGES = [
    "You have a meeting soon! 🌸",
    "Heads up bestie! ✨",
    "Get ready! 💕",
    "Almost time! ⭐",
    "Meeting incoming! 🎀",
]

# ---------------- PATH HELPERS ----------------

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def get_token_path():
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(os.path.dirname(sys.executable), 'token.pickle')
    return os.path.join(os.path.dirname(__file__), 'token.pickle')

# ---------------- GOOGLE AUTH ----------------

def get_service():
    creds = None
    token_path = get_token_path()

    if os.path.exists(token_path):
        with open(token_path, 'rb') as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                resource_path('credentials.json'),
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as f:
            pickle.dump(creds, f)

    return build('calendar', 'v3', credentials=creds)

# ---------------- VOICE (AUDIO FILE) ----------------

def play_voice(meeting_name):
    """
    Plays your custom recorded voice file.
    You can replace voice.mp3 with anything you want.
    """
    try:
        path = resource_path("voice.mp3")
        playsound(path)
    except Exception as e:
        print("Audio error:", e)

# ---------------- STICKER ----------------

def load_sticker():
    path = resource_path("sticker.png")
    img = Image.open(path).convert("RGBA")
    img = img.resize((220, 220))
    return ImageTk.PhotoImage(img)

# ---------------- OVERLAY ----------------

def show_overlay(meeting_name):
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.configure(bg="black")  # will be invisible due to transparency
    root.wm_attributes("-transparentcolor", "black")

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{sw}x{sh}+0+0")

    canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    sticker = load_sticker()

    x = [-200]

    def animate():
        x[0] += 14

        canvas.delete("all")

        # 🎯 ONLY sticker (no box, no background UI)
        canvas.create_image(
            x[0],
            sh // 2,
            image=sticker
        )
        canvas.image = sticker

        # OPTIONAL: very subtle minimal text (grey, no box)
        if x[0] > sw // 2 - 120:
            canvas.create_text(
                sw // 2,
                sh // 2 + 140,
                text=f"⏰ {meeting_name}",
                fill="#666666",  # neutral grey
                font=("Segoe UI", 12)
            )

        if x[0] < sw + 200:
            root.after(16, animate)
        else:
            root.destroy()

    animate()
    root.mainloop()

# ---------------- CALENDAR CHECK ----------------

def check_meetings():
    try:
        service = get_service()

        now = datetime.datetime.now(datetime.timezone.utc)
        window = now + datetime.timedelta(minutes=20)

        events = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=window.isoformat(),
            singleEvents=True,
            orderBy='startTime'
        ).execute().get('items', [])

        print(f"Checking... {len(events)} events")

        for event in events:
            eid = event['id']
            if eid in notified:
                continue

            start_str = event['start'].get('dateTime')
            if not start_str:
                continue

            start = datetime.datetime.fromisoformat(
                start_str.replace("Z", "+00:00")
            )

            diff = (start - now).total_seconds() / 60

            print(f"{event.get('summary')} in {diff:.1f} min")

            if 0 <= diff <= 20:
                notified.add(eid)
                name = event.get('summary', 'Meeting')

                # popup
                threading.Thread(
                    target=show_overlay,
                    args=(name,),
                    daemon=True
                ).start()

                # 🎧 voice file
                threading.Thread(
                    target=play_voice,
                    args=(name,),
                    daemon=True
                ).start()

    except Exception as e:
        print("Error:", e)

# ---------------- TRAY ICON ----------------

def make_tray_icon():
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([8, 8, 56, 56], fill="#FF69B4")
    return img

# ---------------- SCHEDULER ----------------

def run_scheduler():
    schedule.every(30).seconds.do(check_meetings)
    check_meetings()

    while True:
        schedule.run_pending()
        time.sleep(5)

# ---------------- MAIN ----------------

def main():
    print("Meeting Fairy Voice Mode 🎀 started!")

    threading.Thread(target=run_scheduler, daemon=True).start()

    icon = pystray.Icon(
        "meeting-fairy",
        make_tray_icon(),
        "Meeting Fairy",
        menu=pystray.Menu(
            pystray.MenuItem(
                "Check now",
                lambda: threading.Thread(target=check_meetings, daemon=True).start()
            ),
            pystray.MenuItem(
                "Test popup",
                lambda: threading.Thread(target=show_overlay, args=("Test Meeting",), daemon=True).start()
            ),
            pystray.MenuItem("Quit", lambda: icon.stop())
        )
    )

    icon.run()

if __name__ == "__main__":
    main()