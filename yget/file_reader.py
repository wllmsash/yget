class FileReader(object):
    def read(self, file):
        with open(file) as f:
            return f.read()

    def read_lines(self, file):
        lines = []
        with open(file) as f:
            for line in f:
                lines.append(line)

        return lines
