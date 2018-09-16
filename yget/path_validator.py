import os

class PathValidator:
    def validate_directory(self, path):
        return os.path.isdir(os.path.join(os.getcwd(), path))

    def validate_file(self, path):
        return os.path.isfile(os.path.join(os.getcwd(), path))
