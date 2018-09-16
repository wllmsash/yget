import getopt

class ArgumentParser:
    opt_help = "-h"
    opt_output_directory = "-o"
    opt_url = "-u"
    opt_bookmarks = "-b"
    opt_verbose = "-v"

    opt_help_long = "--help"
    opt_output_directory_long = "--output-directory"
    opt_url_long = "--url"
    opt_bookmarks_long = "--bookmarks"
    opt_verbose_long = "--verbose"
    opt_audio_only_long = "--audio-only"
    opt_wav_long = "--wav"
    opt_mp3_long = "--mp3"
    opt_netrc_long = "--netrc"

    opt_string = "ho:u:b:v"
    opt_long_array = ["help", "output-directory=", "url=", "bookmarks=", "verbose", "audio-only", "wav", "mp3", "netrc"]

    def __init__(self, argv):
        if argv is None or not argv:
            raise ValueError("argv must be non-None and non-empty")

        self.argv = argv

    def make_arguments_invalid_message(self):
        name = self.argv[0]
        args = " ".join(self.argv[1:])

        error_message = ""
        error_message += "{}: invalid arguments '{}'\n".format(name, args)
        error_message += "Try '{} --help' for more information.".format(name)

        return error_message

    def make_help_message(self):
        name = self.argv[0]

        help_message = ""
        help_message += "yget: Downloads YouTube videos.\n"
        help_message += "\n"
        help_message += "Usage: {} [options...] [file]...\n".format(name)
        help_message += "   or: {} [options...] -\n".format(name)
        help_message += "   or: {} [-u <url> | -b <bookmarks_file>] [options...]\n".format(name)

        help_message += "\n"
        help_message += "Files:\n"
        help_message += "  Files should be space separated and contain a line break separated list of YouTube video urls or video ids.\n"
        help_message += "  Playlists are valid urls and all videos in the playlist will be downloaded.\n"
        help_message += "\n"
        help_message += "  If no files are provided or [file]... is -, read from standard input. Use Ctrl-D to signal end of input.\n"
        help_message += "\n"
        help_message += "Valid Urls:\n"
        help_message += "- https://www.youtube.com/watch?v=rdwz7QiG0lk\n"
        help_message += "- rdwz7QiG0lk\n"
        help_message += "- https://www.youtube.com/watch?list=PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        help_message += "- https://www.youtube.com/watch?v=kavB05H3g90&list=PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        help_message += "- PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        help_message += "\n"
        help_message += "Modes:\n"
        help_message += "One and only one mode is required\n"
        help_message += "\n"
        help_message += " -o, --output-directory=OUTPUT_DIRECTORY\n"
        help_message += "     URL of the YouTube video to download\n"
        help_message += " -u, --url=\"URL\"\n"
        help_message += "     URL of the YouTube video to download\n"
        help_message += " -b, --bookmarks=BOOKMARKS_FILE\n"
        help_message += "     Bookmarks formatted file to extract YouTube urls from\n"
        help_message += " -h, --help\n"
        help_message += "     Display help information\n"

        help_message += "\n"
        help_message += "Options:\n"
        help_message += " -v, --verbose      Output youtube_dl messages to stdout\n"
        help_message += "     --audio-only   Download only audio data for the provided url(s)\n"
        help_message += "     --wav          audio-only but with output forced to wav format\n"
        help_message += "     --mp3          audio-only but with output forced to mp3 format\n"
        help_message += "     --netrc        Use .netrc file for authentication\n"
        help_message += "     Entry must follow the format: machine youtube login <username> password <password>\n"

        return help_message

    def parse(self):
        try:
            opts, args = getopt.getopt(self.argv[1:], ArgumentParser.opt_string, ArgumentParser.opt_long_array)
        except getopt.GetoptError:
            return (False, None, None, None)

        mode = None
        output_directory = "."
        has_verbose_option = False
        has_audio_only_option = False
        has_wav_option = False
        has_mp3_option = False
        has_netrc_option = False

        for o, a in opts:
            if o in (ArgumentParser.opt_help, ArgumentParser.opt_help_long):
                mode = ("help", None)
                return (True, mode, None, None)
            elif o in (ArgumentParser.opt_url, ArgumentParser.opt_url_long) and not mode:
                mode = ("url", a.strip())
            elif o in (ArgumentParser.opt_bookmarks, ArgumentParser.opt_bookmarks_long) and not mode:
                mode = ("bookmarks", a.strip())
            elif o in (ArgumentParser.opt_output_directory, ArgumentParser.opt_output_directory_long):
                output_directory = a.strip()
            elif o in (ArgumentParser.opt_verbose, ArgumentParser.opt_verbose_long):
                has_verbose_option = True
            elif o == ArgumentParser.opt_audio_only_long:
                has_audio_only_option = True
            elif o == ArgumentParser.opt_wav_long:
                has_wav_option = True
            elif o == ArgumentParser.opt_mp3_long:
                has_mp3_option = True
            elif o == ArgumentParser.opt_netrc_long:
                has_netrc_option = True

        if mode is None and args and len(args) == 1 and args[0] == "-":
            mode = ("files", [])
        if mode is None and args:
            mode = ("files", args)
        elif mode is None:
            mode = ("files", [])

        return (True, mode, output_directory, (has_verbose_option, has_audio_only_option, has_wav_option, has_mp3_option, has_netrc_option))
