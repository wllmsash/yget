from .helpers import Helpers

class App:
    def __init__(self, argument_parser, bookmarks_parser, downloader_factory, file_reader, input_provider, path_validator, logger):
        self.argument_parser = argument_parser
        self.bookmarks_parser = bookmarks_parser
        self.downloader_factory = downloader_factory
        self.file_reader = file_reader
        self.input_provider = input_provider
        self.path_validator = path_validator
        self.logger = logger

    def run(self):
        arguments_valid, mode_info, output_directory, options = self.argument_parser.parse()

        if not arguments_valid:
            self.logger.write_line(self.argument_parser.make_arguments_invalid_message())
            return 1

        mode, mode_value = mode_info

        if mode == "help":
            self.logger.write_line(self.argument_parser.make_help_message())
            return 0

        if not self.path_validator.validate_directory(output_directory):
            self.logger.write_line("Output directory '{}' does not exist".format(output_directory))
            return 1

        has_verbose_option, has_audio_only_option, has_wav_option, has_mp3_option, has_netrc_option = options

        downloader = self.downloader_factory.make_downloader(output_directory, has_verbose_option, has_netrc_option)

        if mode == "files":
            files = mode_value

            for f in files:
                if not self.path_validator.validate_file(f):
                    self.logger.write_line("Input file '{}' does not exist".format(f))
                    return 1

            urls = []

            if not files:
                while True:
                    line = None
                    try:
                        line = self.input_provider.get_input("")
                        urls.append(line)
                    except EOFError:
                        break
            else:
                for f in files:
                    lines = self.file_reader.read_lines(f)
                    urls.extend(Helpers.strip_strings(lines))

            downloader.download_videos(urls, audio_only=has_audio_only_option, wav=has_wav_option, mp3=has_mp3_option)
        elif mode == "url":
            url = mode_value

            downloader.download_videos([url], audio_only=has_audio_only_option, wav=has_wav_option, mp3=has_mp3_option)
        elif mode == "bookmarks":
            bookmarks_file = mode_value

            if not self.path_validator.validate_file(bookmarks_file):
                self.logger.write_line("Bookmarks file '{}' does not exist".format(bookmarks_file))
                return 1

            bookmarks_file_data = self.file_reader.read(bookmarks_file)
            bookmarks_valid, urls = self.bookmarks_parser.parse(bookmarks_file_data)

            if not bookmarks_valid:
                self.logger.write_line("Bookmarks file '{}' not valid".format(bookmarks_file))
                return 1

            downloader.download_videos(urls, audio_only=has_audio_only_option, wav=has_wav_option, mp3=has_mp3_option)

        return 0
