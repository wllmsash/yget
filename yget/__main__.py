#!/usr/bin/env python3

import sys

from .app import App
from .argument_parser import ArgumentParser
from .bookmarks_parser import BookmarksParser
from .downloader_factory import DownloaderFactory
from .file_reader import FileReader
from .input_provider import InputProvider
from .logger import Logger
from .path_validator import PathValidator

def main(argv):
    input_provider = InputProvider()
    logger = Logger()

    argument_parser = ArgumentParser(argv)
    bookmarks_parser = BookmarksParser(input_provider, logger)
    downloader_factory = DownloaderFactory()
    file_reader = FileReader()
    path_validator = PathValidator()

    app = App(argument_parser, bookmarks_parser, downloader_factory, file_reader, input_provider, path_validator, logger)

    app.run()

if __name__ == '__main__':
    sys.exit(main(sys.argv))
