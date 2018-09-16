from yget.file_reader import FileReader

class MockFileReader(FileReader):
    def __init__(self, read_delegate, read_lines_delegate):
        super(MockFileReader, self).__init__()

        self.read_delegate = read_delegate
        self.read_lines_delegate = read_lines_delegate

    def read(self, file):
        return self.read_delegate(file)

    def read_lines(self, file):
        return self.read_lines_delegate(file)
