import unittest

from collections import deque
from yget.bookmarks_parser import BookmarksParser

from .mock_input_provider import MockInputProvider
from .mock_logger import MockLogger

class TestBookmarksParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_bookmarks_file_data = """
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT! -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>
            </DL><p>
        """

        cls.single_level_single_page_bookmarks_file_data = """
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT! -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 1</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 2</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
            </DL><p>
        """

        cls.single_level_multiple_pages_bookmarks_file_data = """
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT! -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 1</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 2</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 3</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 4</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 5</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 6</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 7</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 8</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 9</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 10</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 11</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
                <DT><H3>Folder 12</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
            </DL><p>
        """

        cls.multiple_level_bookmarks_file_data = """
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT! -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 1</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><H3>Folder 1.1</H3>
                    <DL><p>
                        <DT><A HREF="https://website.com">Website</A>
                        <DT><A HREF="https://website.com">Website</A>
                    </DL><p>
                    <DT><H3>Folder 1.2</H3>
                    <DL><p>
                        <DT><A HREF="https://website.com">Website</A>
                        <DT><A HREF="https://website.com">Website</A>
                    </DL><p>
                </DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 2</H3>
                <DL><p>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
            </DL><p>
        """

        cls.multiple_level_bookmarks_file_data_with_valid_urls = """
            <!DOCTYPE NETSCAPE-Bookmark-file-1>
            <!-- This is an automatically generated file.
                It will be read and overwritten.
                DO NOT EDIT! -->
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
            <TITLE>Bookmarks</TITLE>
            <H1>Bookmarks</H1>
            <DL><p>
                <DT><A HREF="https://youtube.com/watch?v=00000000000">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 1</H3>
                <DL><p>
                    <DT><A HREF="https://youtube.com/watch?v=11111111111">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                    <DT><A HREF="https://youtube.com/watch?v=22222222222">Website</A>
                    <DT><H3>Folder 1.1</H3>
                    <DL><p>
                        <DT><A HREF="https://website.com">Website</A>
                        <DT><A HREF="https://website.com">Website</A>
                    </DL><p>
                    <DT><H3>Folder 1.2</H3>
                    <DL><p>
                        <DT><A HREF="https://youtube.com/watch?v=33333333333&amp;list=0000000000000000000000000000000000">Website</A>
                        <DT><A HREF="https://website.com">Website</A>
                    </DL><p>
                </DL><p>
                <DT><A HREF="https://website.com">Website</A>
                <DT><H3>Folder 2</H3>
                <DL><p>
                    <DT><A HREF="https://youtube.com/watch?list=0000000000000000000000000000000000&amp;v=44444444444">Website</A>
                    <DT><A HREF="https://website.com">Website</A>
                </DL><p>
            </DL><p>
        """

    def make_bookmarks_parser(self, mock_input_provider=None, mock_logger=None):
        if not mock_input_provider:
            mock_input_provider = MockInputProvider(lambda x: "", lambda x: "")

        if not mock_logger:
            mock_logger = MockLogger()

        return BookmarksParser(mock_input_provider, mock_logger)

    def test_parse_with_invalid_data_returns_failure(self):
        make_bookmarks_parser = self.make_bookmarks_parser()

        valid, urls = make_bookmarks_parser.parse("<invalid></file>")

        self.assertFalse(valid)
        self.assertIsNone(urls)

    def test_parse_with_exit_returns_no_urls_and_success(self):
        responses = deque(["0"])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.empty_bookmarks_file_data)

        expected_line_list = ["Enter: Download links in Root", "    0: Exit"]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_with_empty_data_returns_no_urls_and_success(self):
        responses = deque([""])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.empty_bookmarks_file_data)

        expected_line_list = [
            "Enter: Download links in Root",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_with_single_level_single_page_logs_and_returns_correctly(self):
        responses = deque(["0"])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.single_level_single_page_bookmarks_file_data)

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_with_single_level_multiple_pages_logs_and_returns_correctly(self):
        responses = deque(["9", "9", "0"])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.single_level_multiple_pages_bookmarks_file_data)

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    3: Move to Folder 3",
            "    4: Move to Folder 4",
            "    5: Move to Folder 5",
            "    6: Move to Folder 6",
            "    7: Move to Folder 7",
            "    8: Move to Folder 8",
            "    9: Next page",
            "    0: Exit",
            "Enter: Download links in Root",
            "    1: Move to Folder 9",
            "    2: Move to Folder 10",
            "    3: Move to Folder 11",
            "    4: Move to Folder 12",
            "    9: Back to first page",
            "    0: Exit",
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    3: Move to Folder 3",
            "    4: Move to Folder 4",
            "    5: Move to Folder 5",
            "    6: Move to Folder 6",
            "    7: Move to Folder 7",
            "    8: Move to Folder 8",
            "    9: Next page",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_with_multiple_levels_logs_and_returns_correctly(self):
        responses = deque(["1", "0", "0"])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.multiple_level_bookmarks_file_data)

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit",
            "Enter: Download links in Folder 1",
            "    1: Move to Folder 1.1",
            "    2: Move to Folder 1.2",
            "    0: Back to Root",
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_with_single_level_single_page_and_incorrect_option_logs_and_returns_correctly(self):
        responses = deque(["8", "0"])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.single_level_single_page_bookmarks_file_data)

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit",
            "Option not valid"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, [])

    def test_parse_root_no_youtube_urls_returns_correct_urls(self):
        responses = deque([""])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.multiple_level_bookmarks_file_data)

        expected_urls = []

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, expected_urls)

    def test_parse_root_youtube_urls_returns_correct_urls(self):
        responses = deque([""])

        mock_input_provider = MockInputProvider(lambda x: responses.popleft(), lambda x: "")

        mock_logger = MockLogger()

        make_bookmarks_parser = self.make_bookmarks_parser(mock_input_provider=mock_input_provider, mock_logger=mock_logger)

        valid, urls = make_bookmarks_parser.parse(self.multiple_level_bookmarks_file_data_with_valid_urls)

        expected_urls = [
            "https://youtube.com/watch?v=00000000000",
            "https://youtube.com/watch?v=11111111111",
            "https://youtube.com/watch?v=22222222222",
            "https://youtube.com/watch?list=0000000000000000000000000000000000&amp;v=44444444444",
            "https://youtube.com/watch?v=33333333333&amp;list=0000000000000000000000000000000000"
        ]

        expected_line_list = [
            "Enter: Download links in Root",
            "    1: Move to Folder 1",
            "    2: Move to Folder 2",
            "    0: Exit"
        ]

        self.assertListEqual(mock_logger.write_line_calls, expected_line_list)
        self.assertTrue(valid)
        self.assertListEqual(urls, expected_urls)
