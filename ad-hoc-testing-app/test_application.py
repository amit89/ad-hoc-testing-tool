import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from session_manager import SessionManager
from testing_session import TestingSession
from explorer_details import ExplorerDetails


class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.session_manager = SessionManager(self.root)

    def test_save_button_opens_testing_session(self):
        # Simulate clicking the Save button
        self.session_manager.open_testing_session = MagicMock()
        self.session_manager.open_testing_session()
        self.session_manager.open_testing_session.assert_called_once()


class TestTestingSession(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.testing_session = TestingSession(self.root, "Test Session")

    @patch('testing_session.ExplorerDetails')
    def test_open_explorer_details(self, MockExplorerDetails):
        mock_explorer = MockExplorerDetails.return_value
        self.testing_session.open_explorer_details(self.root)
        MockExplorerDetails.assert_called_once_with(self.root)
        mock_explorer.open.assert_called_once()


class TestExplorerDetails(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.explorer_details = ExplorerDetails(self.root)
        self.explorer_details.open()

    @patch('explorer_details.messagebox.showinfo')
    def test_set_charter_and_tester(self, mock_showinfo):
        self.explorer_details.charter_name_entry = MagicMock()
        self.explorer_details.tester_name_entry = MagicMock()
        self.explorer_details.charter_name_entry.get = MagicMock(return_value="Charter1")
        self.explorer_details.tester_name_entry.get = MagicMock(return_value="Tester1")

        self.explorer_details.set_charter_and_tester()
        self.assertEqual(self.explorer_details.session_data["charter_name"], "Charter1")
        self.assertEqual(self.explorer_details.session_data["tester_name"], "Tester1")
        mock_showinfo.assert_called_once_with("Information Saved", "Charter Name and Tester Name saved.")

    @patch('explorer_details.filedialog.askopenfilename')
    @patch('explorer_details.messagebox.showinfo')
    def test_attach_screenshot(self, mock_showinfo, mock_askopenfilename):
        mock_askopenfilename.return_value = "path/to/screenshot.png"
        # Create a dummy file for the test
        with open("path/to/screenshot.png", "wb") as f:
            f.write(b'fake_image_data')

        self.explorer_details.attach_screenshot()
        self.assertIn("screenshot", self.explorer_details.current_action)
        mock_showinfo.assert_called_once_with("Attachment", "Attached: path/to/screenshot.png")

    @patch('explorer_details.messagebox.showinfo')
    def test_save_as_draft(self, mock_showinfo):
        self.explorer_details.note_text = MagicMock()
        self.explorer_details.note_text.get = MagicMock(return_value="Test note")
        self.explorer_details.note_type_var = MagicMock()
        self.explorer_details.note_type_var.get = MagicMock(return_value="IDEA")

        self.explorer_details.save_as_draft()
        actions = self.explorer_details.session_data["actions"]
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0]["note"], "Test note")
        self.assertEqual(actions[0]["note_type"], "IDEA")
        mock_showinfo.assert_called_once_with("Draft Saved", "Your data has been saved as a draft.")

    # Add tests for the timer and end_session functionalities as needed


if __name__ == '__main__':
    unittest.main()
