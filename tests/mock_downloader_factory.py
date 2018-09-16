from yget.downloader_factory import DownloaderFactory

from .mock_downloader import MockDownloader

class MockDownloaderFactory(DownloaderFactory):
    def __init__(self, raise_in_download_videos=None):
        super(MockDownloaderFactory, self).__init__()

        self.downloader = None

        self.raise_in_download_videos = False

        if raise_in_download_videos is not None:
            self.raise_in_download_videos = raise_in_download_videos

    def make_downloader(self, output_directory, verbose, use_netrc):
        self.downloader = MockDownloader(self.raise_in_download_videos)

        return self.downloader
