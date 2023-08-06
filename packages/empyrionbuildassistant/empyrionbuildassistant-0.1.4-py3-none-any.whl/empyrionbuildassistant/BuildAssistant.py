

def copy_dlls(source_folder, target_folder):
    from os import path
    from shutil import copy
    from .lib import DLLS_BEING_COPIED

    for dll in DLLS_BEING_COPIED:
        source_path = path.join(source_folder, dll)
        print(f"copying {dll} to {target_folder}")
        copy(source_path, target_folder)

    print("dll copy complete")


def copy_mod_contents(src_folder, mod_name, empyrion_installation_folder):
    from shutil import copytree, rmtree
    from os import path
    from .lib import EMPYRION_MOD_FOLDER_PATH

    mods_folder_path = path.join(empyrion_installation_folder, EMPYRION_MOD_FOLDER_PATH, mod_name)

    if path.exists(mods_folder_path):
        print(f"removing existing tree at {mods_folder_path}")
        rmtree(mods_folder_path)
        print("old mod removed")

    print(f"copying the tree at {src_folder} to {mods_folder_path}")
    copytree(src_folder, mods_folder_path)
    print("deploy complete")


def clear_logs(empyrion_install_path):
    from shutil import rmtree
    from os import path, listdir
    from .lib import EMPYRION_LOGS_FOLDER_PATH

    logs_path = path.join(empyrion_install_path, EMPYRION_LOGS_FOLDER_PATH)
    folders = listdir(logs_path)
    print("clearing logs")
    for folder in folders:
        folder_path = path.join(logs_path, folder)
        print(f"clearing log folder @ {folder_path}")
        rmtree(folder_path)
    print("logs cleared")


def watch_logs(empyrion_install_path):
    from os import path
    from watchdog.observers.polling import PollingObserver
    from .lib import EMPYRION_LOGS_FOLDER_PATH, FileDiffPrinter

    logs_path = path.join(empyrion_install_path, EMPYRION_LOGS_FOLDER_PATH)

    event_handler = FileDiffPrinter()
    observer = PollingObserver(1.0)
    observer.schedule(event_handler, logs_path, recursive=True)
    observer.start()

    return observer


def launch_server(install_path):
    from os import path
    import psutil
    from .lib import EMPYRION_SERVER_LAUNCHER, EMPYRION_SERVER_ARGS

    process_path = path.join(install_path, EMPYRION_SERVER_LAUNCHER)
    p_args = [process_path] + EMPYRION_SERVER_ARGS

    result = psutil.Popen(p_args, cwd=install_path)

    children = result.children()
    return children


def exec_build_assistant(parsed_args):
    from os import path
    from .lib import get_app_install_path_from_appid, DEDI_SERVER_APPID, EMPYRION_DLL_FOLDER_PATH, terminate_processes

    empyrion_install_path = get_app_install_path_from_appid(DEDI_SERVER_APPID)

    if parsed_args.copyDllsToFolder:
        installed_dlls_folder = path.join(empyrion_install_path, EMPYRION_DLL_FOLDER_PATH)
        copy_dlls(installed_dlls_folder, parsed_args.copyDllsToFolder)

    if parsed_args.bundleAndDeployMod:
        copy_mod_contents(parsed_args.bundleAndDeployMod, parsed_args.modName, empyrion_install_path)

    if parsed_args.clearLogs:
        clear_logs(empyrion_install_path)

    if parsed_args.watchLogs:
        observer = watch_logs(empyrion_install_path)
    else:
        observer = None

    if parsed_args.launchServer:
        children = launch_server(empyrion_install_path)
    else:
        children = None

    if observer or children:
        try:
            t = input()
        finally:
            if children:
                terminate_processes(children)
            if observer:
                observer.stop()
                observer.join()


def construct_arg_parser():
    import argparse

    parser = argparse.ArgumentParser(
        description='scripts to help build and deploy empyrion mods',
        epilog='Note: modname must be specified when using the bundleAndDeployMod option'
    )

    parser.add_argument("--copyDllsToFolder", help="the folder to copied the required dlls to")
    parser.add_argument("--modName", help="the name of the mod being deployed")
    parser.add_argument("--bundleAndDeployMod", help="the folder containing the mod that will be deployed")
    parser.add_argument("-clearLogs", action="store_true", help="clears the logs on the dedi server")
    parser.add_argument("-watchLogs", action="store_true", help="watches the dedi server logs, press enter to exit")
    parser.add_argument("-launchServer", action="store_true", help="launches the dedi server, press enter to kill")

    def result_parser():
        result = parser.parse_args()
        if result.bundleAndDeployMod and not result.modName:
            parser.error('you must specify a modname when using the bundleAndDeployMod option')
        return result

    return result_parser


def main():
    get_parsed_args = construct_arg_parser()
    parsed_args = get_parsed_args()
    exec_build_assistant(parsed_args)


if __name__ == '__main__':
    main()