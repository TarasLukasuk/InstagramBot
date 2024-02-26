import tkinter as tk
from tkinter import ttk
from Bots.Instagram.instagram import InstagramBot
import threading


class InstagramBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Instagram Bot")
        self.inst = None

        # Create a style for the labels
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 12))

        self.label_username = ttk.Label(master, text="Username:")
        self.label_password = ttk.Label(master, text="Password:")
        self.label_message = ttk.Label(master, text="Message:")
        self.label_usernames = ttk.Label(master, text="Usernames (comma-separated):")

        # Create a style for the entry fields
        style.configure("TEntry", font=("Arial", 12))

        self.entry_username = ttk.Entry(master)
        self.entry_password = ttk.Entry(master, show="*")
        self.entry_message = ttk.Entry(master)
        self.entry_usernames = ttk.Entry(master)

        self.label_username.grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_message.grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.label_usernames.grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)

        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.entry_message.grid(row=2, column=1, padx=10, pady=5)
        self.entry_usernames.grid(row=3, column=1, padx=10, pady=5)

        # Create a style for the button with a different color and font
        style.configure("TButton",
                        font=("Arial", 14, "bold"),
                        foreground="Blue",
                        background="#3498db",  # Change the button background color
                        borderwidth=2,
                        relief=tk.GROOVE)

        self.button_run = ttk.Button(master, text="Run Bot", command=self.start_bot_thread, style="TButton")
        self.button_run.grid(row=4, column=1, pady=10)

        # Bind the closing event to on_closing
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.bot_thread = None

    def start_bot_thread(self):
        self.bot_thread = threading.Thread(target=self.run_bot_thread)
        self.bot_thread.start()

    def run_bot_thread(self):
        user_name = self.entry_username.get()
        password = self.entry_password.get()
        message = self.entry_message.get()
        user_names_input = self.entry_usernames.get().split(',')

        self.inst = InstagramBot(message)
        self.inst.login_bot(user_name, password)
        self.inst.find_user(user_names_input)

    def on_closing(self):
        if self.inst:
            self.inst.exit()
        if self.bot_thread and self.bot_thread.is_alive():
            self.bot_thread.join()
        self.master.destroy()