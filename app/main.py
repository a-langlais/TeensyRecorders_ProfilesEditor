import sys
from PySide6.QtWidgets import QApplication
from ui_editor import ProfileEditor
from ini_utils import resource_path

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ini_file = resource_path("initial_profile/Profiles.ini")
    logo_file = resource_path("img/logo_PR.png")

    window = ProfileEditor(str(ini_file), logo_path=str(logo_file))
    window.resize(500, 680)
    window.show()

    sys.exit(app.exec())
