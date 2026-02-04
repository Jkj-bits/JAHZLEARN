import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time

serverurl = "https://seamless-ted-simultaneously.ngrok-free.dev"
username = input("Enter your username: ").strip()


class chatclient:
    def __init__(self, root, username):
        self.username = username
        self.root = root
        self.root.title("JAHZ Chat Client")
        self.root.geometry("800x600")
        self.root.config(bg="#80a285")
        
        self.chatframe = tk.Frame(self.root, bg="#e6bf3e")
        self.chatframe.pack(pady=10)

        self.chatlabel = tk.Label(self.chatframe, text="JAHZ Chatroom", bg="#e6bf3e", font=("Arial", 16))
        self.chatlabel.pack(pady=10)

        self.chattext = tk.Text(self.chatframe, height=20, width=70, state=tk.DISABLED)
        self.chattext.pack(pady=10)

        self.chatentry = tk.Entry(self.chatframe, font=("Arial", 12))
        self.chatentry.pack(pady=10)

        self.sendbutton = tk.Button(self.chatframe, text="Send", font=("Arial", 12), bg="#000000", fg="white", command=self.sendmessage)
        self.sendbutton.pack(pady=10)

        self.running = True
        threading.Thread(target=self.fetchmessages, daemon=True).start()

    def sendmessage(self):
        msg = self.chatentry.get().strip()
        if not msg:
            messagebox.showwarning("Empty Message", "Please enter a message before sending.")
            return
        data = {"user": self.username, "text": msg}
        try:
            response = requests.post(f"{serverurl}/messages", json=data)
            if response.status_code == 200:
                self.chatentry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to send message.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def fetchmessages(self):
        while self.running:
            try:
                response = requests.get(f"{serverurl}/messages")
                if response.status_code == 200:
                    messages = response.json()
                    self.chattext.config(state=tk.NORMAL)
                    self.chattext.delete(1.0, tk.END)
                    for msg in messages:
                        self.chattext.insert(tk.END, f"{msg['user']}: {msg['text']}\n")
                    self.chattext.config(state=tk.DISABLED)
                time.sleep(2)
            except requests.exceptions.RequestException:
                time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    client = chatclient(root, username)
    root.mainloop()


