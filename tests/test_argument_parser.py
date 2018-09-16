import unittest

from yget.argument_parser import ArgumentParser

class TestArgumentParser(unittest.TestCase):
    def make_argument_parser(self, argv):
        return ArgumentParser(argv)

    def test_construction_with_none_argv_throws(self):
        with self.assertRaises(ValueError) as wrapped_e:
            self.make_argument_parser(None)

        self.assertIn("argv must be non-None and non-empty", str(wrapped_e.exception))

    def test_construction_with_empty_argv_throws(self):
        with self.assertRaises(ValueError) as wrapped_e:
            self.make_argument_parser([])

        self.assertIn("argv must be non-None and non-empty", str(wrapped_e.exception))

    def test_construction_with_some_argv_succeeds(self):
        self.make_argument_parser(["yget.py"])

    def test_make_arguments_invalid_message_formatted_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--wrong", "--args"])

        arguments_invalid_message = argument_parser.make_arguments_invalid_message()

        expected_arguments_invalid_message = ""
        expected_arguments_invalid_message += "yget.py: invalid arguments '--wrong --args'\n"
        expected_arguments_invalid_message += "Try 'yget.py --help' for more information."

        self.assertEqual(arguments_invalid_message, expected_arguments_invalid_message)

    def test_make_help_message_formatted_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py"])

        help_message = argument_parser.make_help_message()

        expected_help_message = ""
        expected_help_message += "yget: Downloads YouTube videos.\n"
        expected_help_message += "\n"
        expected_help_message += "Usage: yget.py [options...] [file]...\n"
        expected_help_message += "   or: yget.py [options...] -\n"
        expected_help_message += "   or: yget.py [-u <url> | -b <bookmarks_file>] [options...]\n"

        expected_help_message += "\n"
        expected_help_message += "Files:\n"
        expected_help_message += "  Files should be space separated and contain a line break separated list of YouTube video urls or video ids.\n"
        expected_help_message += "  Playlists are valid urls and all videos in the playlist will be downloaded.\n"
        expected_help_message += "\n"
        expected_help_message += "  If no files are provided or [file]... is -, read from standard input. Use Ctrl-D to signal end of input.\n"
        expected_help_message += "\n"
        expected_help_message += "Valid Urls:\n"
        expected_help_message += "- https://www.youtube.com/watch?v=rdwz7QiG0lk\n"
        expected_help_message += "- rdwz7QiG0lk\n"
        expected_help_message += "- https://www.youtube.com/watch?list=PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        expected_help_message += "- https://www.youtube.com/watch?v=kavB05H3g90&list=PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        expected_help_message += "- PLbpi6ZahtOH5WgR8NbZJtSY6XkO0WQZVe\n"
        expected_help_message += "\n"
        expected_help_message += "Modes:\n"
        expected_help_message += "One and only one mode is required\n"
        expected_help_message += "\n"
        expected_help_message += " -o, --output-directory=OUTPUT_DIRECTORY\n"
        expected_help_message += "     URL of the YouTube video to download\n"
        expected_help_message += " -u, --url=\"URL\"\n"
        expected_help_message += "     URL of the YouTube video to download\n"
        expected_help_message += " -b, --bookmarks=BOOKMARKS_FILE\n"
        expected_help_message += "     Bookmarks formatted file to extract YouTube urls from\n"
        expected_help_message += " -h, --help\n"
        expected_help_message += "     Display help information\n"

        expected_help_message += "\n"
        expected_help_message += "Options:\n"
        expected_help_message += " -v, --verbose      Output youtube_dl messages to stdout\n"
        expected_help_message += "     --audio-only   Download only audio data for the provided url(s)\n"
        expected_help_message += "     --wav          audio-only but with output forced to wav format\n"
        expected_help_message += "     --mp3          audio-only but with output forced to mp3 format\n"
        expected_help_message += "     --netrc        Use .netrc file for authentication\n"
        expected_help_message += "     Entry must follow the format: machine youtube login <username> password <password>\n"

        self.assertEqual(help_message, expected_help_message)

    def test_parse_with_invalid_options_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--wrong", "--args"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_no_additional_argv_entries_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, [])
        self.assertEqual(output_directory, ".")

    def test_parse_with_dash_argv_entry_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, [])
        self.assertEqual(output_directory, ".")

    def test_parse_with_additional_argv_entries_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "URL_1", "URL_2"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, ["URL_1", "URL_2"])
        self.assertEqual(output_directory, ".")

    def test_parse_with_short_help_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-h"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "help")
        self.assertEqual(mode_value, None)

    def test_parse_with_short_help_mode_and_another_mode_parses_as_help_mode(self):
        argument_parser = self.make_argument_parser(["yget.py", "-h", "-b MY_BOOKMARKS"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "help")
        self.assertEqual(mode_value, None)

    def test_parse_with_long_help_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--help"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "help")
        self.assertEqual(mode_value, None)

    def test_parse_with_long_help_mode_and_another_mode_parses_as_help_mode(self):
        argument_parser = self.make_argument_parser(["yget.py", "--help", "-b MY_BOOKMARKS"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "help")
        self.assertEqual(mode_value, None)

    def test_parse_with_short_output_directory_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-o MY_OUTPUT_DIRECTORY"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, [])
        self.assertEqual(output_directory, "MY_OUTPUT_DIRECTORY")

    def test_parse_with_short_output_directory_without_space_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-oMY_OUTPUT_DIRECTORY"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, [])
        self.assertEqual(output_directory, "MY_OUTPUT_DIRECTORY")

    def test_parse_with_long_output_directory_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--output-directory=MY_OUTPUT_DIRECTORY"])

        arguments_valid, mode_info, output_directory, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "files")
        self.assertEqual(mode_value, [])
        self.assertEqual(output_directory, "MY_OUTPUT_DIRECTORY")

    def test_parse_with_short_output_directory_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-o"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_long_output_directory_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--output-directory"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_short_url_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-u MY_URL"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "url")
        self.assertEqual(mode_value, "MY_URL")

    def test_parse_with_short_url_mode_without_space_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-uMY_URL"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "url")
        self.assertEqual(mode_value, "MY_URL")

    def test_parse_with_long_url_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--url=MY_URL"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "url")
        self.assertEqual(mode_value, "MY_URL")

    def test_parse_with_short_url_mode_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-u"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_long_url_mode_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--url"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_short_bookmarks_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-b MY_BOOKMARKS"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "bookmarks")
        self.assertEqual(mode_value, "MY_BOOKMARKS")

    def test_parse_with_short_bookmarks_mode_without_space_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-bMY_BOOKMARKS"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "bookmarks")
        self.assertEqual(mode_value, "MY_BOOKMARKS")

    def test_parse_with_long_bookmarks_mode_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--bookmarks=MY_BOOKMARKS"])

        arguments_valid, mode_info, _, _ = argument_parser.parse()
        mode, mode_value = mode_info

        self.assertTrue(arguments_valid)
        self.assertEqual(mode, "bookmarks")
        self.assertEqual(mode_value, "MY_BOOKMARKS")

    def test_parse_with_short_bookmarks_mode_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-b"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_long_bookmarks_mode_without_value_parses_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--bookmarks"])

        arguments_valid, _, _, _ = argument_parser.parse()

        self.assertFalse(arguments_valid)

    def test_parse_with_short_verbose_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "-v"])

        arguments_valid, _, _, options = argument_parser.parse()
        has_verbose_option, _, _, _, _ = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_verbose_option)

    def test_parse_with_long_verbose_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--verbose"])

        arguments_valid, _, _, options = argument_parser.parse()
        has_verbose_option, _, _, _, _ = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_verbose_option)

    def test_parse_with_audio_only_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--audio-only"])

        arguments_valid, _, _, options = argument_parser.parse()
        _, has_audio_only_option, _, _, _ = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_audio_only_option)

    def test_parse_with_wav_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--wav"])

        arguments_valid, _, _, options = argument_parser.parse()
        _, _, has_wav_option, _, _ = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_wav_option)

    def test_parse_with_mp3_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--mp3"])

        arguments_valid, _, _, options = argument_parser.parse()
        _, _, _, has_mp3_option, _ = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_mp3_option)

    def test_parse_with_netrc_option_sets_correctly(self):
        argument_parser = self.make_argument_parser(["yget.py", "--netrc"])

        arguments_valid, _, _, options = argument_parser.parse()
        _, _, _, _, has_netrc_option = options

        self.assertTrue(arguments_valid)
        self.assertTrue(has_netrc_option)

