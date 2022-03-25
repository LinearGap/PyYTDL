import argparse
from ast import arg
from logging import exception
import os
import tempfile
from tkinter import E
from PyYTDL_Downloader import PyYTDL_Downloader as YTDL
from PyYTDL_Downloader import YTVid

# Callback Method
def download_progress_meter_callback(stream, chunk, bytes_remaining):
    """
    Print out a download meter using the filesize of the current download
    to inform the user of their progress
    """
    percent = ((float(stream.filesize) - bytes_remaining) / stream.filesize)
    blocks = int(percent * 10)
    hashes = ['##' for i in range(blocks)]

    # Print using :> formatter to specify string length to keep blocks at same width
    print(f'Downloading: {int(percent * 100):>3}% complete [ {"".join(hashes):>20} ]')

# -----------------------------------------------------------------------------------------------

class PyYTDL():
    """
    Main entry and control point. This is what is called from the command
    line when the program is run.
    Usage: PyYTDL.py url
    Optional:   [-a] Download audio only. Default = False
                [-hq] Download the highest quality video available. Default = False
                [-o "filename"] Specify the output filename. Default = Video Title
                [-r] Specify the prefered resolution to download. Default = 1080p
                [-p] Open the file after downloading and converting. Default = False
    """
    pass

    def __init__(self):
        # The settings dict to be updated by __parse_args
        self.__settings = {'audio Only':False, 'hq':False, 'filename':'', 'resolution':1080, 'open':False}
        # The YouTube URL to download from
        self.__YTURL = ""
        self.__parse_args()
        self.vid_id = self.get_vid_id(self.__YTURL)

        # Setup the downloader
        self.__downloader = YTDL()

        # Check the video is valid and set the title if so
        self.vid_title = self.__check_valid_YT_ID(self.vid_id)
        print(f'Youtube video found: {self.vid_title}')

        # Get the correct stream object based upon user settings
        self.__streams = self.__get_stream()

        # Register the progress callback
        self.__downloader.add_download_progress_callback(download_progress_meter_callback)

        # Create a temp directory to store the downloaded audio and video
        self.__temp_dir = self.create_temp_directory()

        # Download the streams
        self.__temp_file_paths = self.download_streams(self.__streams, self.__temp_dir)
        print('File download complete')

    def __parse_args(self):
        """
        Parse command line arguments into the settings list
        """
        parser = argparse.ArgumentParser(description="Download and Convert YouTube videos.")
        parser.add_argument('-a', '--audio', dest='a', action='store_true', default=False, help="Download audio track only, discarding any video.")
        parser.add_argument('-hq', '--high_quality', dest='hq', action='store_true', default=False, help="Download the highest quality versions of the video and audio available.")
        parser.add_argument('-o', '--output', dest='o', metavar="Filename", action='store', default="", type=str, help="Specify the output filename and path.")
        parser.add_argument('-r', '--resolution', dest='r', metavar='Resolution', action='store', default=1080, type=int, help="Specify the preferred resolution to download at. Will select closest higher resolution.")
        parser.add_argument('-p', '--open', dest='p', action='store_true', default=False, help="Open the produced file after download and conversion has occured.")

        parser.add_argument('url', metavar='Youtube URL', action='store', type=str, help='The url of the YouTube video to download.')

        args = parser.parse_args()
        self.__settings['audio only'] = args.a
        self.__settings['hq'] = args.hq
        self.__settings['filename'] = args.o
        self.__settings['resolution'] = self.__fix_resolution(args.r)
        self.__settings['open'] = args.p
        self.__YTURL = args.url

    def __fix_resolution(self, resolution) -> int:
        """
        Take the input resolution and convert into a valid resolution target.
        Use rounding to set.
        """
        out_res = 0
        if resolution < 240:
            out_res = 240
        if resolution > 240:
            out_res = 360
        if resolution > 360:
            out_res = 480
        if resolution > 480:
            out_res = 720
        if resolution > 720:
            out_res = 1080
        if resolution > 1080:
            out_res = 1440
        if resolution > 1440:
            out_res = 2160

        return out_res

    def get_vid_id(self, url: str):
        """
        Check the supplied URL is a valid URL. Remove the video identifier and append back to
        YouTube link to ensure safety.
        Return: Extracted video ID
        """
        stripped = ""
        # If the last character is a symbol strip it
        if url[-1].isalnum():
            stripped = url
        else:
            stripped = url[:-1]

        # The video id is the last 11 characters of the YTURL
        ID = stripped[-11:]

        # Check the new URL only contains letters and numbers
        if ID.isalnum():
            return ID
        else:
            raise

    def __check_valid_YT_ID(self, ytid: str):
        """
        Use the PyYTDL_Downloader to check if the extracted id is valid.
        YTDL seturl function raises an exception if the video is invalid,
        if not it returns the title of the video
        """
        title = ""
        try:
            title = self.__downloader.set_URL(f'http://www.youtube.com/{ytid}')
        except exception as e:
            raise e
        
        return title

    def __get_stream(self):
        """
        Using the command-line arguments or defaults, get the matching streams
        Return: Dict{audio: "", video: ""} of YTVid objects for streams
        """

        # List of streams
        DL_streams = self.__downloader.get_streams()
        out_streams = {'audio': None, 'video': None}

        audio_stream = None
        video_stream = None

        # Loop through the streams
        for yt_stream in DL_streams:

            # Audio Streams
            if yt_stream.avtype == "audio":
                if audio_stream == None:
                    audio_stream = yt_stream
                else:
                    if yt_stream.bitrate > audio_stream.bitrate:
                        audio_stream = yt_stream

            # Video Streams
            if not self.__settings['audio only']:
                if yt_stream.avtype == "video":
                    if video_stream == None:
                        video_stream = yt_stream
                    else:
                        if self.__settings['hq']:
                            if yt_stream.resolution > video_stream.resolution:
                                video_stream = yt_stream
                        else:
                            if yt_stream.resolution > video_stream.resolution and yt_stream.resolution <= self.__settings['resolution']:
                                # Higher res than stored stream, but less than or equal to target resolution.
                                # This means the closest match resolution will be output
                                video_stream = yt_stream
                            elif yt_stream.resolution == video_stream.resolution:
                                if yt_stream.bitrate > video_stream.bitrate:
                                    # Same resolution but better bitrate, get this stream
                                    video_stream = yt_stream

                        
        

        out_streams['audio'] = audio_stream
        out_streams['video'] = video_stream
        return out_streams

    def create_temp_directory(self) -> str:
        """
        Create a temporary directory to store the temporary and pre-conversion
        video and audio files
        Returns: String path to temp directory
        """
        temp_dir = tempfile.TemporaryDirectory()
        return temp_dir.name

    def download_streams(self, streams, directory) -> dict:
        """
        Download the streams and return a dict for the files
        Returns: Dict {'audio':, 'video':}
        """

        file_paths = {'audio': '', 'video': ''}

        # First download the audio stream as this will be kept in place everytime
        print('Downloading audio file:')
        try:
            audio_path = self.__downloader.download_stream(streams['audio'], filename="audio.pyA", download_directory=directory)
        except exception as e:
            raise e

        # Download video if that is also needed
        if not self.__settings['audio only']:
            print('Downloading video file:')
            try:
                video_path = self.__downloader.download_stream(streams['video'], filename="video.pyV", download_directory=directory)
            except exception as e:
                raise e

        file_paths['audio'] = audio_path
        file_paths['video'] = video_path

        return file_paths


# ----------------------------------------------------------------------------------
def main():
    ytdl = PyYTDL()

if __name__ == '__main__':
    main()