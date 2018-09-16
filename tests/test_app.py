import unittest

from collections import deque
from yget.app import App

from .mock_argument_parser import MockArgumentParser
from .mock_bookmarks_parser import MockBookmarksParser
from .mock_downloader_factory import MockDownloaderFactory
from .mock_file_reader import MockFileReader
from .mock_input_provider import MockInputProvider
from .mock_path_validator import MockPathValidator
from .mock_logger import MockLogger

class TestApp(unittest.TestCase):
    def make_app(self,
        mock_argument_parser=None,
        mock_bookmarks_parser=None,
        mock_downloader_factory=None,
        mock_file_reader=None,
        mock_input_provider=None,
        mock_path_validator=None,
        mock_logger=None):
        if not mock_argument_parser:
            mock_argument_parser = MockArgumentParser()

        if not mock_bookmarks_parser:
            mock_bookmarks_parser = MockBookmarksParser()

        if not mock_downloader_factory:
            mock_downloader_factory = MockDownloaderFactory()

        lines_for_file = {
            "FILE_1": ["LINE_1", "LINE_2"],
            "FILE_2": ["LINE_3", "LINE_4"]
        }

        if not mock_file_reader:
            mock_file_reader = MockFileReader(lambda x: "", lambda x: lines_for_file[x])

        if not mock_input_provider:
            mock_input_provider = MockInputProvider(lambda x: "", lambda x: "")

        if not mock_path_validator:
            mock_path_validator = MockPathValidator(lambda x: True, lambda x: True)

        if not mock_logger:
            mock_logger = MockLogger()

        return App(mock_argument_parser, mock_bookmarks_parser, mock_downloader_factory, mock_file_reader, mock_input_provider, mock_path_validator, mock_logger)

    def stdin_get_response(self, responses):
        if len(responses) > 0:
            return responses.popleft()

        raise EOFError()

    def test_app_called_with_invalid_arguments_logs_and_returns_error_code(self):
        mock_argument_parser = MockArgumentParser()

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["ARGUMENTS_INVALID_MESSAGE"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 1)

    def test_app_in_help_mode_logs_and_returns_success_code(self):
        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_help_mode()

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["HELP_MESSAGE"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 0)

    def test_app_with_non_existent_output_directory_logs_and_returns_error_code(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode([], options)
        mock_argument_parser.set_output_directory("MY_OUTPUT_DIRECTORY")

        mock_path_validator = MockPathValidator(lambda x: False, lambda x: True)

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_path_validator=mock_path_validator, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["Output directory 'MY_OUTPUT_DIRECTORY' does not exist"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 1)

    def test_app_in_help_mode_with_non_existent_output_directory_logs_and_returns_error_code(self):
        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_help_mode()

        mock_path_validator = MockPathValidator(lambda x: False, lambda x: True)

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_path_validator=mock_path_validator, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["HELP_MESSAGE"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_non_existent_file_logs_and_returns_error_code(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_path_validator = MockPathValidator(lambda x: True, lambda x: False)

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_path_validator=mock_path_validator, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["Input file 'FILE_1' does not exist"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 1)

    def test_app_in_files_mode_with_no_files_accepts_stdin(self):
        options = (False, False, False, False, False)
        responses = deque(["URL_1", "URL_2"])

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode([], options)

        mock_downloader_factory = MockDownloaderFactory()

        mock_input_provider = MockInputProvider(lambda x: self.stdin_get_response(responses), lambda x: "")

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory, mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["URL_1", "URL_2"])
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_audio_only_with_successful_download_returns(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["LINE_1", "LINE_2", "LINE_3", "LINE_4"])
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_audio_only_with_raised_download_propagates(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_files_mode_with_wav_with_successful_download_returns(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["LINE_1", "LINE_2", "LINE_3", "LINE_4"])
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_wav_with_raised_download_propagates(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_files_mode_with_mp3_with_successful_download_returns(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["LINE_1", "LINE_2", "LINE_3", "LINE_4"])
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_mp3_with_raised_download_propagates(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_files_mode_with_successful_download_returns(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["LINE_1", "LINE_2", "LINE_3", "LINE_4"])
        self.assertEqual(code, 0)

    def test_app_in_files_mode_with_raised_download_propagates(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_files_mode(["FILE_1", "FILE_2"], options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_url_mode_with_audio_only_with_successful_download_returns(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["MY_URL"])
        self.assertEqual(code, 0)

    def test_app_in_url_mode_with_audio_only_with_raised_download_propagates(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_url_mode_with_wav_with_successful_download_returns(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["MY_URL"])
        self.assertEqual(code, 0)

    def test_app_in_url_mode_with_wav_with_raised_download_propagates(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_url_mode_with_mp3_with_successful_download_returns(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["MY_URL"])
        self.assertEqual(code, 0)

    def test_app_in_url_mode_with_mp3_with_raised_download_propagates(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_url_mode_with_successful_download_returns(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["MY_URL"])
        self.assertEqual(code, 0)

    def test_app_in_url_mode_with_raised_download_propagates(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_url_mode("MY_URL", options)

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_bookmarks_mode_with_non_existent_bookmarks_return_error_code(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_path_validator = MockPathValidator(lambda x: True, lambda x: False)

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_path_validator=mock_path_validator, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["Bookmarks file 'MY_BOOKMARKS' does not exist"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 1)

    def test_app_in_bookmarks_mode_with_invalid_bookmarks_return_error_code(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_logger = MockLogger()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_logger=mock_logger)

        code = app.run()

        expected_line_list = ["Bookmarks file 'MY_BOOKMARKS' not valid"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertEqual(code, 1)

    def test_app_in_bookmarks_mode_with_audio_only_with_successful_download_returns(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["URL_1", "URL_2"])
        self.assertEqual(code, 0)

    def test_app_in_bookmarks_mode_with_audio_only_with_raised_download_propagates(self):
        options = (False, True, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_bookmarks_mode_with_wav_with_successful_download_returns(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["URL_1", "URL_2"])
        self.assertEqual(code, 0)

    def test_app_in_bookmarks_mode_with_wav_with_raised_download_propagates(self):
        options = (False, False, True, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_bookmarks_mode_with_mp3_with_successful_download_returns(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["URL_1", "URL_2"])
        self.assertEqual(code, 0)

    def test_app_in_bookmarks_mode_with_mp3_with_raised_download_propagates(self):
        options = (False, False, False, True, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)

    def test_app_in_bookmarks_mode_with_successful_download_returns(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory()

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        code = app.run()

        mock_downloader = mock_downloader_factory.downloader

        self.assertListEqual(mock_downloader.download_video_calls, ["URL_1", "URL_2"])
        self.assertEqual(code, 0)

    def test_app_in_bookmarks_mode_with_raised_download_propagates(self):
        options = (False, False, False, False, False)

        mock_argument_parser = MockArgumentParser()
        mock_argument_parser.set_bookmarks_mode("MY_BOOKMARKS", options)

        mock_bookmarks_parser = MockBookmarksParser()
        mock_bookmarks_parser.set_valid(["URL_1", "URL_2"])

        mock_downloader_factory = MockDownloaderFactory(raise_in_download_videos=True)

        app = self.make_app(mock_argument_parser=mock_argument_parser, mock_bookmarks_parser=mock_bookmarks_parser, mock_downloader_factory=mock_downloader_factory)

        raised = False

        try:
            app.run()
        except:
            raised = True

        self.assertTrue(raised)
