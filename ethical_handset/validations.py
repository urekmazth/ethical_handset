import platform


def verify_os():
    os_name = platform.system()

    return os_name == "Linux" or os_name == "Darwin" or os_name == "Linux2"
