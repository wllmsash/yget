import glob
import os
import sys
import youtube_dl

class DownloadLogger(object):
    def __init__(self, verbose):
        self.verbose = verbose

    def debug(self, msg):
        if self.verbose:
            print(msg)

    def warning(self, msg):
        if self.verbose:
            print(msg)

    def error(self, msg):
        if self.verbose:
            print(msg)

class DownloaderOptionsBuilder:
    default_download_options = {
        "format": "mp4/bestvideo",
        "no_color": True,
        "outtmpl": "%(title)s (%(id)s).%(ext)s",
        "postprocessors": [{'key': 'FFmpegMetadata'}]
    }
    default_output_directory = "."

    def __init__(self):
        self.download_options = DownloaderOptionsBuilder.default_download_options
        self.output_directory = DownloaderOptionsBuilder.default_output_directory

    def make_download_options(self):
        options = self.download_options.copy()
        options["outtmpl"] = os.path.join(self.output_directory, options["outtmpl"])
        return options

    def set_output_directory(self, output_directory):
        self.output_directory = output_directory

    def set_authentication_params(self, authentication_params):
        self.download_options["username"] = authentication_params["username"]
        self.download_options["password"] = authentication_params["password"]

    def set_progress_hook(self, progress_hook):
        self.download_options["progress_hooks"] = [progress_hook]

    def set_logger(self, logger):
        self.download_options["logger"] = logger

    def set_audio_only(self):
        self.download_options["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "best"
        },
        {'key': 'FFmpegMetadata'}]

    def set_wav(self):
        self.download_options["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "wav"
        },
        {'key': 'FFmpegMetadata'}]

    def set_mp3(self):
        self.download_options["postprocessors"] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': "mp3"
        },
        {'key': 'FFmpegMetadata'}]

    def set_use_netrc(self):
        self.download_options["usenetrc"] = True

    def set_album(self, album):
        self.download_options["postprocessor_args"] = ["-metadata", "album={}".format(album)]

class Downloader:
    def __init__(self, output_directory, verbose, use_netrc, authentication_provider):
        self.started_download = False

        self.output_directory = output_directory
        self.verbose = verbose
        self.use_netrc = use_netrc

        self.authentication_provider = authentication_provider

    def create_download_options(self):
        download_options = DownloaderOptionsBuilder()
        download_options.set_output_directory(self.output_directory)
        download_options.set_progress_hook(self.download_status)
        download_options.set_logger(DownloadLogger(self.verbose))

        if self.use_netrc:
            download_options.set_use_netrc()

        return download_options

    def download_videos(self, urls, audio_only=False, wav=False, mp3=False):
        downloaded = 0
        skipped = 0
        failed = 0

        authentication_params = {}

        for url in urls:
            should_request_authentication = not self.use_netrc
            has_requested_authentication = False

            download_options = self.create_download_options()

            if wav:
                download_options.set_wav()
            elif mp3:
                download_options.set_mp3()
            elif audio_only:
                download_options.set_audio_only()

            album = None
            infos = []

            while True:
                if authentication_params:
                    download_options.set_authentication_params(authentication_params)

                try:
                    with youtube_dl.YoutubeDL(download_options.make_download_options()) as youtube_downloader:
                        info = youtube_downloader.extract_info(url, download=False)

                        # Set album to playlist title
                        if "entries" in info:
                            album = info["title"]

                            for entry in info["entries"]:
                                infos.append(entry)
                        else:
                            album = "YouTube"

                            infos.append(info)

                        download_options.set_album(album)

                        break
                except youtube_dl.utils.DownloadError as e:
                    if "Please sign in to view this video" in str(e) or "Please enter your password" in str(e):
                        print("({}, {}) {}".format(url, None, str(e)))
                        if should_request_authentication and not has_requested_authentication:

                            has_requested_authentication = True

                            if not self.authentication_provider.request_authentication_parameters(authentication_params):
                                break

                            continue

                    print("({}, {}) {}".format(url, None, str(e)))

                    break
                except Exception as e:
                    print("({}, {}) {}".format(url, None, str(e)))

                    break

            if not infos:
                failed += 1
                continue

            for info in infos:
                while True:
                    if authentication_params:
                        download_options.set_authentication_params(authentication_params)

                    try:
                        with youtube_dl.YoutubeDL(download_options.make_download_options()) as youtube_downloader:
                            filename = youtube_downloader.prepare_filename(info)

                            root, _ = os.path.splitext(os.path.join(os.getcwd(), filename))
                            existing_files = glob.glob(root + ".*")

                            has_part = False

                            if existing_files:
                                for existing_file in existing_files:
                                    _, extension = os.path.splitext(existing_file)

                                    if "part" in extension:
                                        has_part = True
                                        break

                                if not has_part:
                                    skipped += 1
                                    break

                            youtube_downloader.download([info["id"]])
                            downloaded += 1
                            break
                    except youtube_dl.utils.DownloadError as e:
                        if "Please sign in to view this video" in str(e) or "Please enter your password" in str(e):
                            print("({}, {}) {}".format(url, info["id"], str(e)))
                            if should_request_authentication and not has_requested_authentication:

                                has_requested_authentication = True

                                if not self.authentication_provider.request_authentication_parameters(authentication_params):
                                    break

                                continue

                        failed += 1
                        print("({}, {}) {}".format(url, info["id"], str(e)))

                        break
                    except Exception as e:
                        print("({}, {}) {}".format(url, None, str(e)))

                        break

        if downloaded > 0:
            sys.stdout.write("\n")
            sys.stdout.flush()

        print("")
        print("Downloaded " + str(downloaded) + " video(s), skipped " + str(skipped) + " video(s), failed " + str(failed) + " video(s)")

    def download_status(self, info):
        try:
            if info["status"] == "downloading":
                if "total_bytes" in info:
                    current_percentage = info["downloaded_bytes"] * 100.0 / info["total_bytes"]
                else:
                    current_percentage = "?"
                self.download_status_message(info["filename"], current_percentage)
            elif info["status"] == "finished":
                self.download_status_message(info["filename"], 100, True)
                self.started_download = False
        except Exception as e:
            print("Download status error")
            print(e)

    def download_status_message(self, file_name, current_percentage, new_line=False):
        if not self.started_download:
            print("Downloading " + file_name)

        self.started_download = True

        end_of_line = "\r"

        sys.stdout.write("[" + "%.2f" % current_percentage + "%]" + end_of_line)

        sys.stdout.flush()
