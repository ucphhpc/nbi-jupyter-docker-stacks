import os
import shutil


def makedirs(path):
    try:
        os.makedirs(os.path.expanduser(path))
        return True, "Created: {}".format(path)
    except Exception as err:
        return False, "Failed to create the directory path: {} - {}".format(path, err)
    return False, "Failed to create the directory path: {}".format(path)


def load(path, mode="r", readlines=False, handler=None, **load_kwargs):
    try:
        with open(path, mode) as fh:
            if handler:
                return handler.load(fh, **load_kwargs)
            if readlines:
                return fh.readlines()
            return fh.read()
    except Exception as err:
        print("Failed to load file: {} - {}".format(path, err))
    return False


def write(path, content, mode="w", mkdirs=False, handler=None, **handler_kwargs):
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path) and mkdirs:
        if not makedirs(dir_path):
            return False
    try:
        with open(path, mode) as fh:
            if handler:
                handler.dump(content, fh, **handler_kwargs)
            else:
                if isinstance(content, (list, set)):
                    for line in content:
                        fh.write(line)
                else:
                    fh.write(content)
        return True
    except Exception as err:
        print("Failed to save file: {} - {}".format(path, err))
    return False


def remove(path):
    try:
        if exists(path):
            os.remove(os.path.expanduser(path))
            return True, "Removed file: {}".format(path)
    except Exception as err:
        return False, "Failed to remove file: {} - {}".format(path, err)
    return False, "Failed to remove file: {}".format(path)


def removedir(path):
    try:
        if exists(path):
            os.rmdir(os.path.expanduser(path))
            return True, "Removed directory: {}".format(path)
    except Exception as err:
        return False, "Failed to remove directory: {} - {}".format(path, err)
    return False, "Failed to remove directory: {}".format(path)


def exists(path):
    return os.path.exists(os.path.expanduser(path))


def chmod(path, mode, **kwargs):
    try:
        os.chmod(os.path.expanduser(path), mode, **kwargs)
    except Exception as err:
        return (
            False,
            "Failed to set permissions: {} on: {} - {}".format(mode, path, err),
        )
    return True, "Set the path: {} with permissions: {}".format(path, mode)


def copy(original, target):
    # Copy path to target
    try:
        shutil.copyfile(original, target)
    except Exception as err:
        return (
            False,
            "Failed to copy file: {} to: {} - {}".format(original, target, err),
        )
    return True, "Copied file: {} to: {}".format(original, target)
