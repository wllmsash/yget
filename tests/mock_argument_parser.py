from yget.argument_parser import ArgumentParser

class MockArgumentParser(ArgumentParser):
    def __init__(self):
        super(MockArgumentParser, self).__init__([""])

        self.arguments_valid = False
        self.mode_info = None
        self.output_directory = None
        self.options = None

    def set_help_mode(self):
        self.arguments_valid = True
        self.mode_info = ("help", None)

    def set_files_mode(self, files, options):
        self.arguments_valid = True
        self.mode_info = ("files", files)
        self.options = options

    def set_url_mode(self, url, options):
        self.arguments_valid = True
        self.mode_info = ("url", url)
        self.options = options

    def set_bookmarks_mode(self, bookmarks, options):
        self.arguments_valid = True
        self.mode_info = ("bookmarks", bookmarks)
        self.options = options

    def set_output_directory(self, output_directory):
        self.output_directory = output_directory

    def make_arguments_invalid_message(self):
        return "ARGUMENTS_INVALID_MESSAGE"

    def make_help_message(self):
        return "HELP_MESSAGE"

    def parse(self):
        return (self.arguments_valid, self.mode_info, self.output_directory, self.options)
