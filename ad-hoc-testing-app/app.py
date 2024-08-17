import tkinter as tk
from session_manager import SessionManager


def main():
    root = tk.Tk()
    root.title("Session Manager App")  # Set the title of the main window

    # Initialize the SessionManager with the root window
    app = SessionManager(root)

    # Start the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()
