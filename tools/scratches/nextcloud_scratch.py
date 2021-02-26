from webdav3.client import Client
import os
from dotenv import load_dotenv
import lzma
from datetime import datetime
from zipfile import ZipFile, ZIP_LZMA
import re
from textwrap import dedent
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


date_regex = re.compile(r"(?P<year>20\d\d).*?(?P<month>[01]\d).*?(?P<day>[0-3]\d)")


# client.verify = False  # To not check SSL certificates (Default = True)


def compress_log_dir(path):
    zip_file_name = os.path.basename(path) + '_logs.7z'
    zip_file_path = os.path.join(path, zip_file_name)
    if os.path.isfile(zip_file_path) is True:
        os.remove(zip_file_path)
    with ZipFile(zip_file_path, 'w', compression=ZIP_LZMA) as zippy:
        for file in os.scandir(path):
            if file.is_file() and file.name.endswith('txt'):
                zippy.write(file.path, arcname=file.name)
    for file in os.scandir(path):
        if file.is_file() and not file.name.endswith('.7z'):
            os.remove(file.path)


def download_ressource(paths):
    resource = paths[0].resource(paths[1])
    resource.write(paths[2])


def synch_server(name: str):
    to_download = []
    LOGS_FOLDER_NAME = os.getenv('AS_LOG_FOLDER')
    COMPRESS = os.getenv('AS_LOG_COMPRESS') == "1"
    SINCE_DATE = datetime.strptime(os.getenv('AS_LOG_SINCE_DATA'), "%Y-%m-%d")
    OPTIONS = {
        'webdav_hostname': f"https://antistasi.de/dev_drive/remote.php/dav/files/{os.getenv('AS_LOG_USERNAME')}/",
        'webdav_login': os.getenv('AS_LOG_USERNAME'),
        'webdav_password': os.getenv('AS_LOG_PASSWORD')
    }
    client = Client(OPTIONS)
    save_path = os.path.join(LOGS_FOLDER_NAME, name)
    retrieve_path = f'Antistasi_Community_Logs/{name}/Server'
    if os.path.isdir(save_path) is False:
        os.makedirs(save_path)
    for rfile_name in client.list(retrieve_path):
        match = date_regex.search(rfile_name)
        if match:
            date = datetime.strptime(f"{match.group('year')}-{match.group('month')}-{match.group('day')}", "%Y-%m-%d")
            if date >= SINCE_DATE:
                to_download.append((client, f"{retrieve_path}/{rfile_name}", os.path.join(save_path, rfile_name)))
    with ThreadPoolExecutor(12) as pool:
        list(pool.map(download_ressource, to_download))
    if COMPRESS is True:
        compress_log_dir(save_path)


def synch_logs():
    load_dotenv('antistasi_log_synch.env')
    server_to_pull_raw = os.getenv('AS_LOG_SERVER_TO_SYNCH')
    server_to_pull = list(map(lambda x: x.strip(), server_to_pull_raw.split(',')))

    for server in server_to_pull:
        synch_server(server)


if __name__ == '__main__':
    if os.path.isfile('antistasi_log_synch.env') is False:
        with open('antistasi_log_synch.env', 'w') as f:
            f.write(dedent("""  AS_LOG_FOLDER=antistasi_logs
                                AS_LOG_USERNAME=
                                AS_LOG_PASSWORD=
                                AS_LOG_COMPRESS=1
                                AS_LOG_SERVER_TO_SYNCH=Mainserver_1, Testserver_1
                                AS_LOG_SINCE_DATA=2021-01-01"""))
        print('provided "antistasi_log_synch.env" file, please fill it out, keep it in this directory and start the script again afterwards')
    else:
        synch_logs()
