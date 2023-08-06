import vdf
import io
import typing
from watchdog.events import LoggingEventHandler, FileSystemEventHandler

DEDI_SERVER_APPID = '530870'
EGS_APPID = '383120'
EMPYRION_DLL_FOLDER_PATH = 'DedicatedServer/EmpyrionDedicated_Data/Managed'
EMPYRION_MOD_FOLDER_PATH = 'Content/Mods'
EMPYRION_LOGS_FOLDER_PATH = 'Logs'
EMPYRION_SERVER_LAUNCHER = 'EmpyrionLauncher.exe'
EMPYRION_SERVER_ARGS = ['-startDediWithGfx']

DLLS_BEING_COPIED = [
    'Mif.dll',
    'ModApi.dll',
    'UnityEngine.CoreModule.dll'
]


def get_steam_install_path():
    from winreg import ConnectRegistry, HKEY_LOCAL_MACHINE, OpenKeyEx, QueryValueEx
    root = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    steam_software_key = OpenKeyEx(root, r"SOFTWARE\Wow6432Node\Valve\Steam")
    install_path, type_ = QueryValueEx(steam_software_key, "InstallPath")
    return install_path


def get_library_folders(install_path: str):
    from os import path
    steamapps_folder_location = path.join(install_path, 'steamapps')
    steamapps_location = path.join(steamapps_folder_location, 'libraryfolders.vdf')
    with open(steamapps_location) as libraryfolders_stream:
        libraries_manifest = vdf.load(libraryfolders_stream)

    numeric_keys = [i for i in libraries_manifest.keys() if i.isnumeric()]
    other_paths = [libraries_manifest[i] for i in numeric_keys]

    result = [steamapps_folder_location]
    result += other_paths

    return result


def find_folder_with_app_manifest(library_folders, appid):
    from os import path
    looking_for_file = f'appmanifest_{appid}.acf'

    for a_path in library_folders:
        candidate_path = path.join(a_path, looking_for_file)
        if path.exists(candidate_path):
            return candidate_path

    return None


def get_app_install_path_from_folders_and_appid(library_folders, appid):
    from os import path
    import vdf

    candidate_path = find_folder_with_app_manifest(library_folders, appid)

    if not candidate_path:
        raise Exception(f"Empyrion with AppID {appid} was not found on this system's Steam installation")

    with open(candidate_path) as appmanifest_stream:
        appmanifest = vdf.load(appmanifest_stream)

    installdir = appmanifest['AppState']['installdir']
    base_folder = path.dirname(candidate_path)

    return path.join(base_folder, 'common', installdir)


def get_app_install_path_from_appid(appid):
    install_path = get_steam_install_path()
    library_folders = get_library_folders(install_path)
    empyrion_install_path = get_app_install_path_from_folders_and_appid(library_folders, appid)
    return empyrion_install_path


def read_until_newline(a_file_pointer: typing.Type[io.IOBase], a_start = 0):
    from sys import getsizeof
    tracker = a_start
    a_file_pointer.seek(tracker)

    for line in a_file_pointer.readlines():
        tracker += len(line)
        yield (line, tracker)


def get_header(src_path):
    import pathlib
    pure_path = pathlib.PurePath(src_path)

    return f"{pure_path.parent.name}/{pure_path.name}"


def print_from_offset(src_path, offset):
    header = get_header(src_path)

    with open(src_path, 'r') as fp:
        for line in read_until_newline(fp, offset):
            print(f"{header}-{line[0]}".rstrip('\n'))
            result = line[1]

    return result


class FileDiffPrinter(FileSystemEventHandler):
    file_lengths = dict()

    def on_created(self, event):

        if event.is_directory:
            return

        new_offset = print_from_offset(event.src_path, 0)
        self.file_lengths[event.src_path] = new_offset

    def on_modified(self, event):
        if event.is_directory:
            return

        last_length = self.file_lengths.get(event.src_path, None)
        if last_length is None:
            new_offset = print_from_offset(event.src_path, 0)
        else:
            new_offset = print_from_offset(event.src_path, last_length)
        self.file_lengths[event.src_path] = new_offset


def terminate_processes(children):
    import os
    import signal

    for child in children:
        try:
            killresult = os.kill(child.pid, signal.CTRL_C_EVENT)
        except Exception as e:
            print(e)