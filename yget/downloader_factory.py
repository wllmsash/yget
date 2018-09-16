from .authentication_provider import AuthenticationProvider
from .downloader import Downloader
from .input_provider import InputProvider

class DownloaderFactory(object):
    def make_downloader(self, output_directory, verbose, use_netrc):
        return Downloader(output_directory, verbose, use_netrc, AuthenticationProvider(InputProvider()))
