from yget.bookmarks_parser import BookmarksParser

class MockBookmarksParser(BookmarksParser):
    def __init__(self):
        super(MockBookmarksParser, self).__init__(None, None)

        self.valid = False
        self.urls = []

    def set_valid(self, urls):
        self.valid = True
        self.urls = urls

    def parse(self, bookmarks_file):
        if self.valid:
            return (True, self.urls)

        return (False, None)
