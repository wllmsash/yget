# yget: A YouTube video and audio downloader

A python application for downloading video and audio from YouTube.
Downloaded files will have a small amount of metadata appended to improve browsing experience in media players.

## Usage

### Requirements

This project requires the following external dependencies:

* [python3](https://www.python.org/download/releases/3.0/)
* [ffmpeg](https://www.ffmpeg.org/)

All other dependencies can be installed through `pip3`, the python package manager bundled with `python3`.

### Running From the Command Line

Before running you will need to install project dependencies through `pip3`:

    pip3 install -r requirements.txt

You can run the yget library as an application with the following command:

    python3 -m yget [options...] [file]...

For example:

    python3 -m yget a-file-full-of-links-to-download.txt

Standard input (stdin) is supported in any of the following ways:

    python3 -m yget [options...]
    python3 -m yget [options...] -
    python3 -m yget [options...] < a-file.txt

yget can also be used to extract a single URL or playlist with:

    python3 -m yget -u rdwz7QiG0lk [options...]

or a bookmarks file, such as the one exported from Google Chrome, with:

    python3 -m yget -b my-exported-bookmarks.html [options...]

For all the options available, see:

    python3 -m yget --help

### Automated Testing

A small amount of automated testing is included in this project and can be run with:

    ./run_tests.sh

or

    ./run_coverage.sh

If you are interest in further configuring any of the testing, peek inside the above files.

The automated testing included is not exhaustive.

## Useful Development Resources

A list of the resources I found useful when developing this project as a python beginner.

* [Python Project Structure](https://realpython.com/python-application-layouts/)
* [Running Python Unit Tests](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure)
