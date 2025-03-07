import os

def get_executables_in_path():
    """Returns a list of executable files found in the directories listed in the PATH environment variable."""
    path_variable = os.environ.get('PATH', '')
    path_directories = path_variable.split(os.pathsep)
    executables = []

    for directory in path_directories:
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if os.path.isfile(filepath) and os.access(filepath, os.X_OK):
                    executables.append(filename)
    return executables

if __name__ == "__main__":
    executable_list = get_executables_in_path()
    for executable in executable_list:
        print(executable)
