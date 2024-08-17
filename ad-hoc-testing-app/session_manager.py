import tkinter as tk
from tkinter import ttk
from testing_session import TestingSession


class SessionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Session Manager")
        self.root.geometry("400x300")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Session:", font=("Arial", 14)).pack(pady=20)
        self.session_name_entry = tk.Entry(self.root, width=30, font=("Arial", 14))
        self.session_name_entry.pack(pady=10)

        save_button = ttk.Button(self.root, text="Save", command=self.open_testing_session)
        save_button.pack(pady=20)

    def open_testing_session(self):
        session_name = self.session_name_entry.get()
        self.root.withdraw()
        TestingSession(self.root, session_name).open()

