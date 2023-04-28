from pathlib import Path
from move import move_file
import shutil
import sys


SORTING_DICT = {'picture': ['.jpg', '.bmp', '.png'],
                'video': ['.avi', '.mp4', '.wmv', '.3gpp'],
                'documents': ['.doc', '.docx', '.xls', '.xlsx', '.txt', '.pdf', '.pptx'],
                'music': ['.mp3', '.wav', '.flac', '.aac', '.ogg', 'amr'],
                'archives': ['.zip', '.rar', '.gz', '.tar'],
                'other': []}


def get_category(file: Path):
    extensions = file.suffix.lower()
    for cat, exts in SORTING_DICT.items():
        if extensions in exts:
            return cat
    return 'other'


def sort_folder(path: Path, target_path: Path):
    for item in [p for p in path.glob("*") if p.name not in SORTING_DICT.keys()]:
        if item.is_dir():
            sort_folder(item, target_path)
            item.rmdir()
        else:
            category = get_category(item)
            new_place = move_file(item, target_path, category)
            if category == 'archives' and new_place.parent.exists():
                shutil.unpack_archive(new_place, new_place.parent / new_place.stem)


def main():
    try:
        path = Path(input("Please provide a path to the directory you want to sort: "))
    except IndexError:
        print("Sorry, take a path as a parameter")
        return None

    if not path.exists():
        print(f"Path {path} not exists")
        return None

    sort_folder(path, path)


if __name__ == "__main__":
    main()