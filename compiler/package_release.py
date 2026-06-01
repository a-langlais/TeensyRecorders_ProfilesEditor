import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def parse_args():
    parser = argparse.ArgumentParser(description="Package PyInstaller output as a release archive.")
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-file", required=True, type=Path)
    return parser.parse_args()


def main():
    args = parse_args()
    files = [path for path in args.input_dir.rglob("*") if path.is_file()]
    if not files:
        raise SystemExit(f"No build output found in {args.input_dir}")

    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(args.output_file, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(args.input_dir))


if __name__ == "__main__":
    main()
