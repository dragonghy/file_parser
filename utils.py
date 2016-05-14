import os


def get_filename_from_path(path):
    path = os.path.basename(path)
    filename, ext = os.path.splitext(path)
    return filename

