import tkinter as tk
from tkinter import ttk
from explorer_details import ExplorerDetails

class TestingSession:
    def __init__(self, root, session_name):
        self.root = root
        self.session_name = session_name

    def open(self):
        testing_session = tk.Toplevel(self.root)
        testing_session.title("Testing Session")
        testing_session.geometry("400x300")

        tk.Label(testing_session, text="Tester Assistance", font=("Arial", 14)).pack(pady=20)
        ttk.Button(testing_session, text="EXECUTE").pack(pady=10)
        ttk.Button(testing_session, text="EXPLORE", command=lambda: self.open_explorer_details(testing_session)).pack(pady=10)

    def open_explorer_details(self, testing_session):
        testing_session.destroy()
        ExplorerDetails(self.root).open()
