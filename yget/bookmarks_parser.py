import io
import re

from collections import deque
from xml import etree

class BookmarksParser(object):
    def __init__(self, input_provider, logger):
        self.input_provider = input_provider
        self.logger = logger

        self.youtube_url_regex = re.compile("youtube..*/(watch|playlist)?")

    def parse(self, bookmarks_file_data):
        # Force valid XML
        bookmarks_file_data = bookmarks_file_data.replace("<p>", "").replace("<P>", "").replace("<dt>", "<dt></dt>").replace("<DT>", "<DT></DT>")
        start = max(bookmarks_file_data.find("<dl>"), bookmarks_file_data.find("<DL>"))
        bookmarks_file_data = bookmarks_file_data[start:]

        # Fixes Chrome bookmarks file in XMLParser
        bookmarks_file_data = bookmarks_file_data.replace("&", "&amp;")

        bookmarks = None

        try:
            bookmarks = self.create_bookmarks(bookmarks_file_data)
        except etree.ElementTree.ParseError:
            return (False, None)

        breadcrumbs = [bookmarks[0]]
        last_folder = None
        reset_folder = False
        folders = None

        while True:
            current_folder = breadcrumbs[-1]
            valid_options = []

            if last_folder != current_folder or reset_folder:
                folders = deque(current_folder["folders"])
                reset_folder = False

            last_folder = current_folder

            self.logger.write_line("Enter: Download links in {}".format(current_folder["name"]))

            has_pages = len(current_folder["folders"]) > 8

            i = 1
            while len(folders) > 0 and i < 9:
                folder = folders.popleft()

                valid_options.append((str(i), folder))

                self.logger.write_line("    {}: Move to {}".format(i, folder["name"]))
                i += 1

            if has_pages and len(folders) > 0:
                valid_options.append(("9", None))

                self.logger.write_line("    9: Next page")
            elif has_pages:
                valid_options.append(("9", None))

                self.logger.write_line("    9: Back to first page")

            if len(breadcrumbs) > 1:
                valid_options.append(("0", None))

                self.logger.write_line("    0: Back to {}".format(breadcrumbs[-2]["name"]))
            else:
                valid_options.append(("0", None))

                self.logger.write_line("    0: Exit")

            self.logger.write_empty_line()

            continue_navigation = True
            get_urls = True

            while True:
                option_input = self.input_provider.get_input("Select an option: ")

                if not option_input:
                    continue_navigation = False
                    break

                matched_option = next(filter(lambda x: x[0] == option_input, valid_options), None)

                if matched_option is not None:
                    option, folder = matched_option

                    if option == "9":
                        if len(folders) == 0:
                            reset_folder = True
                    elif option == "0":
                        if len(breadcrumbs) > 1:
                            breadcrumbs.pop()
                        else:
                            continue_navigation = False
                            get_urls = False
                    else:
                        breadcrumbs.append(folder)

                    break
                else:
                    self.logger.write_line("Option not valid")

                self.logger.write_empty_line()

            if not continue_navigation:
                break

            self.logger.write_empty_line()

        urls = []

        if get_urls:
            folders = deque([breadcrumbs[-1]])

            while len(folders) > 0:
                folder = folders.popleft()

                for link in folder["links"]:
                    if self.youtube_url_regex.search(link):
                        urls.append(link)

                folders.extend(folder["folders"])

        return (True, urls)

    def create_bookmarks(self, bookmarks_file_data):
        root = etree.ElementTree.fromstring(bookmarks_file_data)

        bookmarks = []
        queue = deque([(root, "Root", bookmarks)])

        while len(queue) > 0:
            element, name, parent_folders = queue.popleft()

            folders = []
            links = []

            parent_folders.append({
                "name": name,
                "folders": folders,
                "links": links
            })

            last_element_was_dt = False
            last_element = None

            for child in element:
                if child.tag.lower() == "dt":
                    last_element_was_dt = True
                elif last_element_was_dt:
                    if child.tag.lower() == "a":
                        case_insensitive_attributes = dict(zip(map(lambda x: x.lower(), child.attrib.keys()), child.attrib.values()))
                        links.append(case_insensitive_attributes["href"])

                    last_element_was_dt = False
                    last_element = child
                elif child.tag.lower() == "dl":
                    queue.append((child, last_element.text.strip(), folders))

                    last_element = None

        """
        print_queue = deque([(0, bookmarks)])

        while len(print_queue) > 0:
            (n, items) = print_queue.popleft()

            for item in items:
                print((" " * n * 2) + item["name"])

                for link in item["links"]:
                    print((" " * n * 2) + "- " + link)

                print_queue.append((n + 1, item["folders"]))
        """

        return bookmarks
