import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import base64
import os


class ExplorerDetails:
    def __init__(self, root):
        self.root = root
        self.session_data = {
            "charter_name": "",
            "tester_name": "",
            "actions": []
        }
        self.current_action = {}
        self.remaining_time = None  # Holds remaining time in seconds

    def open(self):
        self.explorer_details = tk.Toplevel(self.root)
        self.explorer_details.title("Explorer Details")
        self.explorer_details.geometry("600x600")

        tk.Label(self.explorer_details, text="CHARTER NAME:", font=("Arial", 12)).pack(pady=10)
        self.charter_name_entry = tk.Entry(self.explorer_details, width=40, font=("Arial", 12))
        self.charter_name_entry.pack(pady=5)

        tk.Label(self.explorer_details, text="TESTER NAME:", font=("Arial", 12)).pack(pady=10)
        self.tester_name_entry = tk.Entry(self.explorer_details, width=40, font=("Arial", 12))
        self.tester_name_entry.pack(pady=5)

        ttk.Button(self.explorer_details, text="Set Charter and Tester", command=self.set_charter_and_tester).pack(
            pady=10)

        tk.Label(self.explorer_details, text="TAKE A NOTE:", font=("Arial", 12)).pack(pady=10)
        self.note_text = tk.Text(self.explorer_details, width=50, height=5, font=("Arial", 12))
        self.note_text.pack(pady=5)

        tk.Label(self.explorer_details, text="NOTE TYPE:", font=("Arial", 12)).pack(pady=10)
        self.note_type_var = tk.StringVar()
        note_type_frame = tk.Frame(self.explorer_details)
        note_type_frame.pack(pady=5)
        ttk.Radiobutton(note_type_frame, text="IDEA", variable=self.note_type_var, value="IDEA").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(note_type_frame, text="PROBLEM", variable=self.note_type_var, value="PROBLEM").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(note_type_frame, text="DEFECT", variable=self.note_type_var, value="DEFECT").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(note_type_frame, text="QUESTION", variable=self.note_type_var, value="QUESTION").pack(side=tk.LEFT, padx=5)

        tk.Label(self.explorer_details, text="SET LIMIT:", font=("Arial", 12)).pack(pady=10)
        time_limit_frame = tk.Frame(self.explorer_details)
        time_limit_frame.pack(pady=5)
        ttk.Button(time_limit_frame, text="30 mins", command=lambda: self.start_timer(30)).pack(side=tk.LEFT, padx=5)
        ttk.Button(time_limit_frame, text="45 mins", command=lambda: self.start_timer(45)).pack(side=tk.LEFT, padx=5)

        self.timer_label = tk.Label(self.explorer_details, text="", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        tk.Label(self.explorer_details, text="ACTION:", font=("Arial", 12)).pack(pady=10)
        action_frame = tk.Frame(self.explorer_details)
        action_frame.pack(pady=5)

        ttk.Button(action_frame, text="SCREENSHOT", command=self.attach_screenshot).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="SAVE AS DRAFT", command=self.save_as_draft).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="END SESSION", command=self.end_session).pack(side=tk.LEFT, padx=5)

    def set_charter_and_tester(self):
        self.session_data["charter_name"] = self.charter_name_entry.get()
        self.session_data["tester_name"] = self.tester_name_entry.get()
        messagebox.showinfo("Information Saved", "Charter Name and Tester Name saved.")

    def attach_screenshot(self):
        file_path = filedialog.askopenfilename(
            title="Select a Screenshot",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            self.current_action["screenshot"] = {
                "image_data": encoded_string,
                "file_name": os.path.basename(file_path)
            }

            messagebox.showinfo("Attachment", f"Attached: {file_path}")

    def start_timer(self, minutes):
        self.remaining_time = minutes * 60  # Set the timer in seconds
        self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0:
            mins, secs = divmod(self.remaining_time, 60)
            self.timer_label.config(text=f"Time left: {mins:02}:{secs:02}")
            self.remaining_time -= 1
            # Schedule the update_timer to run after 1 second
            self.explorer_details.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Time's up!")
            messagebox.showwarning("Session Timeout", "Session timeout limit has reached.")

    def save_as_draft(self):
        note = self.note_text.get("1.0", tk.END).strip()
        note_type = self.note_type_var.get()

        if note_type:
            self.current_action["note"] = note
            self.current_action["note_type"] = note_type
            self.session_data["actions"].append(self.current_action.copy())

            self.note_text.delete("1.0", tk.END)
            self.note_type_var.set("")
            self.current_action.clear()

            messagebox.showinfo("Draft Saved", "Your data has been saved as a draft.")
        else:
            messagebox.showwarning("Note Type Missing", "Please select a note type.")

    def end_session(self):
        self.generate_html_report()
        self.explorer_details.destroy()
        self.root.deiconify()

    def generate_html_report(self):
        report_content = f"""
        <html>
        <head>
            <title>Explorer Session Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                .note {{
                    border: 1px solid #ddd;
                    padding: 10px;
                    margin-bottom: 10px;
                }}
                .hidden {{
                    display: none;
                }}
            </style>
            <script>
                function filterNotes() {{
                    var filter = document.getElementById("noteTypeFilter").value;
                    var notes = document.getElementsByClassName("note");

                    for (var i = 0; i < notes.length; i++) {{
                        if (filter === "" || notes[i].getAttribute("data-type") === filter) {{
                            notes[i].classList.remove("hidden");
                        }} else {{
                            notes[i].classList.add("hidden");
                        }}
                    }}
                }}
            </script>
        </head>
        <body>
            <h1>Explorer Session Report</h1>
            <p><strong>Charter Name:</strong> {self.session_data['charter_name']}</p>
            <p><strong>Tester Name:</strong> {self.session_data['tester_name']}</p>

            <label for="noteTypeFilter">Filter by Note Type:</label>
            <select id="noteTypeFilter" onchange="filterNotes()">
                <option value="">All</option>
                <option value="IDEA">IDEA</option>
                <option value="PROBLEM">PROBLEM</option>
                <option value="DEFECT">DEFECT</option>
                <option value="QUESTION">QUESTION</option>
            </select>

            <hr>
        """

        for entry in self.session_data["actions"]:
            note_type = entry.get("note_type", "")
            note_text = entry.get("note", "")
            screenshot = entry.get("screenshot", None)

            report_content += f"""
            <div class="note" data-type="{note_type}">
                <p><strong>Note Type:</strong> {note_type}</p>
                <p><strong>Note:</strong> {note_text}</p>
            """

            if screenshot:
                report_content += f"""
                <p><strong>Screenshot attached:</strong></p>
                <img src="data:image/png;base64,{screenshot['image_data']}" alt="{screenshot['file_name']}" width="300"><br>
                """

            report_content += "</div>"

        report_content += "</body></html>"

        with open("testing_report.html", "w") as file:
            file.write(report_content)

        messagebox.showinfo("Report Generated", "Explorer session report saved as testing_report.html")

