from pathlib import Path
import shutil
from threading import Thread, Semaphore
import logging
import argparse

EXTENSIONS = {
    "images": ['.jpeg', '.png', '.jpg', '.svg'],
    "video": ['.avi', '.mp4', '.mov', '.mkv'],
    "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    "music": ['.mp3', '.ogg', '.wav', '.amr'],
    "archives": ['.zip', '.gz', '.tar'],
    "others": []
}


def normalize(word):
    result = ''
    table = {'А': 'A', 'а': 'a', 'Б': 'B', 'б': 'b', 'В': 'V', 'в': 'v', 'Г': 'G', 'г': 'g', 'Д': 'D', 'д': 'd',
             'Е': 'E', 'е': 'e', 'Ё': 'E', 'ё': 'e', 'Ж': 'J', 'ж': 'j', 'З': 'Z', 'з': 'z', 'И': 'I', 'и': 'i',
             'Й': 'J', 'й': 'j', 'К': 'K', 'к': 'k', 'Л': 'L',
             'л': 'l', 'М': 'M', 'м': 'm', 'Н': 'N', 'н': 'n', 'О': 'O', 'о': 'o', 'П': 'P', 'п': 'p', 'Р': 'R',
             'р': 'r', 'С': 'S', 'с': 's', 'Т': 'T',
             'т': 't', 'У': 'U', 'у': 'u', 'Ф': 'F', 'ф': 'f', 'Х': 'H', 'х': 'h', 'Ц': 'TS', 'ц': 'c', 'Ч': 'CH',
             'ч': 'ch', 'Ш': 'SH', 'ш': 'sh',
             'Щ': 'SCH', 'щ': 'sch', 'Ъ': '', 'ъ': '', 'Ы': 'Y', 'ы': 'y', 'Ь': '', 'ь': '', 'Э': 'E', 'э': 'e',
             'Ю': 'YU',
             'ю': 'yu', 'Я': 'YA', 'я': 'ya', 'Є': 'JE', 'є': 'je', 'І': 'I', 'і': 'i', 'Ї': 'JI', 'ї': 'ji', 'Ґ': 'G',
             'ґ': 'g', '.': '.', '\\': '\\', ':': ':',
             'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'x': 'x'}
    for i in word:
        if i not in table.values():
            if i in table.keys():
                result += table[i]
            elif '0' <= i <= '9':
                result += i
            else:
                result += '_'
        else:
            result += i
    return result


parser = argparse.ArgumentParser(description="Sorter")
parser.add_argument('-s', '--source', required=True)
parser.add_argument('-o', '--output', default='destination')
args = vars(parser.parse_args())
source = args.get('source')
output = args.get('output')


folders = []


def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def sort_file(path: Path, condition):
    with condition:
        for el in path.iterdir():
            if el.is_file():
                name = normalize(el.name)
                ext = el.suffix
                for key, val in EXTENSIONS.items():
                    new_path = output_folder / key
                    if ext in val:
                        try:
                            new_path.mkdir(exist_ok=True, parents=True)
                            shutil.copyfile(el, new_path / name)
                            logging.debug(f'Copied {name}')
                            break
                        except OSError as e:
                            logging.error(e)
                else:
                    try:
                        others_path = output_folder / 'others'
                        others_path.mkdir(exist_ok=True, parents=True)
                        shutil.copyfile(el, others_path / name)
                    except OSError as e:
                        logging.error(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    grabs_folder(base_folder)

    threads = []
    pool = Semaphore(6)
    for folder in folders:
        th = Thread(target=sort_file, args=(folder, pool,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    logging.debug(f'Sorted in {output_folder}')