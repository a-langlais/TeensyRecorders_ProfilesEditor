import argparse
import os
import PyInstaller.__main__

sep = ";" if os.name == "nt" else ":"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))


def parse_args():
    parser = argparse.ArgumentParser(description="Build TeensyProfilesEditor with PyInstaller.")
    parser.add_argument("--dist-dir", default=os.path.join(ROOT_DIR, "dist"))
    parser.add_argument("--work-dir", default=os.path.join(ROOT_DIR, "build", "pyinstaller"))
    parser.add_argument("--spec-dir", default=os.path.join(ROOT_DIR, "build", "spec"))
    return parser.parse_args()


args = parse_args()

PyInstaller.__main__.run([
    os.path.join(ROOT_DIR, "app", "main.py"),
    "--onefile",
    "--noconsole",
    "--name=TeensyProfilesEditor",
    "--clean",
    f"--distpath={args.dist_dir}",
    f"--workpath={args.work_dir}",
    f"--specpath={args.spec_dir}",
    f"--add-data={os.path.join(ROOT_DIR,'initial_profile')}{sep}initial_profile",
    f"--add-data={os.path.join(ROOT_DIR,'img')}{sep}img",
    f"--icon={os.path.join(ROOT_DIR,'img','logo_PR_ico.ico')}",
    f"--paths={os.path.join(ROOT_DIR, 'app')}"
])
