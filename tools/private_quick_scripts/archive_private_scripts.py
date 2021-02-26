import lzma
import shutil
import zipfile
from gidtools.gidfiles import pathmaker
from tempfile import TemporaryDirectory
import os
from dotenv import load_dotenv
import logging
import sys
from datetime import datetime

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


load_dotenv(pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\tools\_project_devmeta.env"))
timestamp = datetime.now().strftime("[%Y-%m-%d_%H-%M]")
source_dir = pathmaker(os.getenv("WORKSPACEDIR"), "tools", "private_quick_scripts")
THIS_FILE = pathmaker(__file__)
archive_name = "personal_scripts_archive_" + timestamp
end_folder = pathmaker(r"D:\Dropbox\hobby\Modding\Programs\Github\My_Repos\Antipetros_Discord_Bot_new\misc\archive\personal_scripts")


def print_folder(src, names):
    print(src)
    return shutil.ignore_patterns(".venv", ".pytest_cache", ".vscode", "__pycache__", ".git", os.path.basename(THIS_FILE))(src, names)


def make_archive_name(name: str, round_num: int = 0) -> str:
    arch_name = name if round_num == 0 else f"{name}_{round_num}"
    path = pathmaker(end_folder, arch_name + '.zip')
    if os.path.isfile(path):
        return make_archive_name(name, round_num + 1)
    return arch_name


def make_local_backup():
    with TemporaryDirectory() as tmpdir:
        path = pathmaker(tmpdir, 'temp_backup_folder')

        print("starting copy of directory")
        shutil.copytree(source_dir, path, ignore=print_folder)
        print("creating archive")
        _archive_name = make_archive_name(archive_name)
        archive = shutil.make_archive(_archive_name, 'zip', path, logger=root)
        print("moving archive")
        shutil.move(archive, end_folder)
        if os.path.isfile(pathmaker(end_folder, _archive_name + '.zip')) is True and os.path.getsize(pathmaker(end_folder, _archive_name + '.zip')) != 0:

            shutil.rmtree(source_dir)
        if os.path.isdir(source_dir) is False:
            os.makedirs(source_dir)


if __name__ == '__main__':
    make_local_backup()
