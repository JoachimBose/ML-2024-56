import os

def list_directories(path):
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories

def list_files(path):
    files = [d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d))]
    return files

def is_compile(path):
    return any(list_files(path), lambda f: f == "compile.py")

def get_directories():
    path = os.getcwd() + '/test'

    all_directories = []

    for directory in list_directories(path):
        path_temp = path + '/' + directory
        directories = filter(map(list_directories(path_temp), lambda d: './test/' + directory + '/' + d), is_compile)
        all_directories.append(directories)
    return all_directories