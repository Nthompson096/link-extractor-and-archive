import sys
import time
import random
import re
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QLineEdit,
    QLabel, QVBoxLayout, QWidget, QTextBrowser, QSpinBox
)
from PyQt6.QtCore import QThread, pyqtSignal
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Helper Functions
def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 503, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def extract_archived_url(response_text):
    match = re.search(r'https://archive\.ph/\S+', response_text)
    return match.group(0) if match else None


# Worker Thread for Archiving
class ArchiveWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, int)

    def __init__(self, urls, wait_time):
        super().__init__()
        self.urls = urls
        self.wait_time = wait_time

    def run(self):
        archive_url = "https://archive.ph/submit/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        successful_archives = 0
        failed_archives = 0

        for i, url in enumerate(self.urls):
            for attempt in range(3):
                try:
                    self.progress.emit(f"Processing URL {i + 1}/{len(self.urls)}: {url}")
                    response = requests_retry_session().post(
                        archive_url,
                        data={"url": url, "capture_all": "on"},
                        headers=headers,
                        timeout=60,
                        verify=False
                    )
                    response.raise_for_status()

                    archived_url = extract_archived_url(response.text)
                    if archived_url:
                        successful_archives += 1
                        self.progress.emit(f"Archived: {url} -> {archived_url}")
                        break
                except Exception as e:
                    self.progress.emit(f"Failed to archive: {url}, Attempt {attempt + 1}, Error: {e}")
                    wait_time = (2 ** attempt) + random.random()
                    time.sleep(wait_time)
            else:
                failed_archives += 1

            time.sleep(self.wait_time)

        self.finished.emit(successful_archives, failed_archives)


# Main GUI Application
class ArchiveApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Archive.ph GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # File Selection
        self.file_label = QLabel("Select a file containing URLs:")
        self.file_path = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        # Single URL Input
        self.single_url_label = QLabel("Or enter a single URL to archive:")
        self.single_url_input = QLineEdit()
        self.archive_single_button = QPushButton("Archive Single URL")
        self.archive_single_button.clicked.connect(self.archive_single_url)

        # Wait Time Input
        self.wait_label = QLabel("Wait time between requests (seconds):")
        self.wait_input = QSpinBox()
        self.wait_input.setMinimum(1)
        self.wait_input.setValue(10)

        # Start Button
        self.start_button = QPushButton("Start Archiving from File")
        self.start_button.clicked.connect(self.start_archiving)

        # Output Log
        self.output_log = QTextBrowser()

        # Add widgets to layout
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.file_path)
        self.layout.addWidget(self.browse_button)
        self.layout.addWidget(self.single_url_label)
        self.layout.addWidget(self.single_url_input)
        self.layout.addWidget(self.archive_single_button)
        self.layout.addWidget(self.wait_label)
        self.layout.addWidget(self.wait_input)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.output_log)

        self.urls = []

    def browse_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select URL File", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.file_path.setText(file_path)
            try:
                with open(file_path, 'r') as file:
                    self.urls = file.read().splitlines()
                self.output_log.append(f"Loaded {len(self.urls)} URLs from {file_path}")
            except Exception as e:
                self.output_log.append(f"Error reading file: {e}")

    def start_archiving(self):
        if not self.urls:
            self.output_log.append("No URLs to process. Please load a valid file.")
            return

        wait_time = self.wait_input.value()
        self.set_ui_enabled(False)  # Disable UI during processing
        self.output_log.append("Starting archiving process...")
        self.worker = ArchiveWorker(self.urls, wait_time)
        self.worker.progress.connect(self.update_log)
        self.worker.finished.connect(self.archive_finished)
        self.worker.start()

    def archive_single_url(self):
        url = self.single_url_input.text().strip()
        if not url:
            self.output_log.append("Please enter a URL.")
            return

        self.set_ui_enabled(False)  # Disable UI during processing
        self.output_log.append(f"Starting to archive single URL: {url}")
        self.worker = ArchiveWorker([url], 0)  # No wait time for single URL
        self.worker.progress.connect(self.update_log)
        self.worker.finished.connect(self.single_archive_finished)
        self.worker.start()

    def update_log(self, message):
        self.output_log.append(message)

    def archive_finished(self, successful, failed):
        self.set_ui_enabled(True)  # Re-enable UI
        self.output_log.append(f"Archiving complete. Successful: {successful}, Failed: {failed}")

    def single_archive_finished(self, successful, failed):
        self.set_ui_enabled(True)  # Re-enable UI
        self.output_log.append("Single URL archiving complete.")
        if successful > 0:
            self.output_log.append("The URL was successfully archived!")
        else:
            self.output_log.append("Failed to archive the URL.")

    def set_ui_enabled(self, enabled):
        """Enable or disable UI elements."""
        self.file_path.setEnabled(enabled)
        self.browse_button.setEnabled(enabled)
        self.single_url_input.setEnabled(enabled)
        self.archive_single_button.setEnabled(enabled)
        self.wait_input.setEnabled(enabled)
        self.start_button.setEnabled(enabled)


# Run the Application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArchiveApp()
    window.show()
    sys.exit(app.exec())
