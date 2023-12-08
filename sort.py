from pathlib import Path
import sys
from threading import Thread
import timeit

CATEGORIES = {'images': ['.jpeg', '.png', '.jpg', '.svg'],
              'video': ['.avi', '.mp4', '.mov', '.mkv'],
              'documents': ['.doc', '.docx','.txt', '.pdf', '.xlsx', '.pptx'],
              'audio': ['.mp3', '.ogg', '.wav', '.amr'],
              'archives': ['.zip', '.gz', '.tar']}

result_know = []
result_dont_know = []

def get_categories(file:Path):
    ext = file.suffix.lower()
    for cat, exst in CATEGORIES.items():
        if ext in exst:
            result_know.append(ext)
            print(cat, file)
            return cat
    result_dont_know.append(ext)
    print('Other', file)
    return 'Other'


def move_file(file:Path, category, root_dir:Path):
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    file.replace(target_dir.joinpath(file.name)) 


def sort_folder(path:Path):
    for element in path.glob('**/*'):
        if element.is_file():
            category = get_categories(element)
            th = Thread(target=move_file, args=(element, category, path))
            th.start()

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return 'Not param for folder'
    
    if not path.exists():
        return 'Folder is not exists'
    
    sort_folder(path)

    print(f'Idintifield {set(result_know)}')
    print(f'Not Idintifield {set(result_dont_know)}')

if __name__ == '__main__':
    threads = []
    main()