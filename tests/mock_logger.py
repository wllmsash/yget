from yget.logger import Logger

class MockLogger(Logger):
    def __init__(self):
        super(MockLogger, self).__init__()

        self.write_empty_line_calls = []
        self.write_line_calls = []

    def write_empty_line(self):
        self.write_empty_line_calls.append(None)

    def write_line(self, line):
        self.write_line_calls.append(line)
