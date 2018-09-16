from yget.downloader import Downloader

class MockDownloader(Downloader):
    def __init__(self, raise_in_download_videos):
        super(MockDownloader, self).__init__(None, None, None, None)

        self.raise_in_download_videos = raise_in_download_videos

        self.download_video_calls = []

    def download_videos(self, urls, audio_only=None, wav=None, mp3=None):
        for url in urls:
            self.download_video_calls.append(url)

        if self.raise_in_download_videos:
            raise "ERROR"
