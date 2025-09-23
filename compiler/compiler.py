import os
import PyInstaller.__main__

sep = ";" if os.name == "nt" else ":"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
OUT_DIR = os.path.join(ROOT_DIR, "build")

PyInstaller.__main__.run([
    os.path.join(ROOT_DIR, "app", "TR_configurator.py"),
    "--onefile",
    "--noconsole",
    "--name=TeensyProfilesEditor",
    "--clean",
    f"--add-data={os.path.join(ROOT_DIR,'initial_profile')}{sep}initial_profile",
    f"--add-data={os.path.join(ROOT_DIR,'fonts')}{sep}fonts",
    f"--add-data={os.path.join(ROOT_DIR,'img')}{sep}img",
    f"--icon={os.path.join(ROOT_DIR,'img','logo_PR_ico.ico')}"
])