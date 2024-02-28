import os

def list_directories(path):
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories

def list_files(path):
    files = [d for d in os.listdir(path) if os.path.isfile(os.path.join(path, d))]
    return files

def is_compile(path):
    return any(filter((lambda f: f == "compile.py"), list_files(path)))

def get_directories():
    path = os.getcwd() + '/test'
    
    all_directories = []

    for directory in list_directories(path):
        print(directory)
        path_temp = path + '/' + directory
        directories = list(filter(is_compile, map((lambda d: './test/' + directory + '/' + d), list_directories(path_temp))))
        all_directories.append(directories)
    return all_directories

if(__name__ == "__main__"):
    for i in get_directories():
        print(i)
