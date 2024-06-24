import sys
import subprocess
import requests
import asyncio
from PyQt6.QtCore import QUrl, QCoreApplication, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt6.QtWebEngineCore import QWebEnginePage

class LoadingPage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    
    def toHtml(self, _):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    font-size: 24px;
                    color: red
                }
            </style>
        </head>
        <body>
            Loading...
        </body>
        </html>
        """

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("FaceLive AI")

        self.faceLive_process = subprocess.Popen(["python", "./run.py"], text=True, creationflags=subprocess.CREATE_NO_WINDOW)

        QCoreApplication.instance().aboutToQuit.connect(self.close_faceLive_process)
        
        # Tạo QWebEngineView
        self.browser = QWebEngineView()
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        self.setLayout(layout)

        self.setFixedSize(1024, 700)

        self.browser.setPage(LoadingPage(self))

    async def run(self, url):
        # load FaceLive App URL
        await self.check_faceLive_processed(url)

    async def check_faceLive_processed(self, url):
        while not self.check_url_accessibility(url):
            continue

        self.browser.setUrl(QUrl(url))  # URL mặc định

        return True
    
    def check_url_accessibility(self, url):
        try:
            response = requests.get(url)
            return response.status_code == 200  # Trả về True nếu mã trạng thái là 200 (OK)
        except requests.exceptions.RequestException:
            return False

    def close_faceLive_process(self):
        self.faceLive_process.terminate()  # Gửi tín hiệu kết thúc đến subprocess
        self.faceLive_process.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    faceLive_url = "http://127.0.0.1:7860"
    asyncio.run(window.run(faceLive_url))

    sys.exit(app.exec())
