import signal
import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from ui_editor import ProfileEditor
from ini_utils import resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    signal.signal(signal.SIGINT, lambda *_: app.quit())
    # Réveille périodiquement la boucle Qt pour laisser Python traiter SIGINT
    sigint_timer = QTimer()
    sigint_timer.start(200)
    sigint_timer.timeout.connect(lambda: None)

    ini_file = resource_path("initial_profile/Profiles.ini")
    logo_file = resource_path("img/logo_PR.png")

    window = ProfileEditor(str(ini_file), logo_path=str(logo_file))
    window.resize(500, 820)
    window.show()

    sys.exit(app.exec())
