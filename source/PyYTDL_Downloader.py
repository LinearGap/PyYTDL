from logging import exception
import os
from pytube import YouTube as PYT

class YTVid():
    """
    Object that will contain information about each available stream available
    for the supplied urls\n
    Tag = Specific identifier for that video stream\n
    Mime_type = The multimedia type\n
    Resolution = The resolution of the video\n
    Bitrate = The video bitrate of the stream\n
    AVType = What type of stream is this Audio/Video\n
    Is_Progresive = Is this a progressive type stream that contains audio and video\n
    Video_codec = What video codec is this stream encoded with\n
    Audio_codec = What audio codec is this stream encoded with\n
    Filesize = How big is the full stream\n
    FPS = The frames per second of the stream
    """
    def __init__(self):
        self.tag = 0
        self.mime_type = ""
        self.resolution = 0
        self.bitrate = ""
        self.avtype = ""
        self.is_progressive = False
        self.video_codec = ""
        self.audio_codec = ""
        self.filesize = 0
        self.fps = 0

class PyYTDL_Downloader():
    """
    The downloader class that will handle getting information about videos from
    YouTube and will also handle the downloading of the video and audio tracks
    """

    def __init__(self):
        self.__YTV = None

    def set_URL(self, URL):
        """
        Set the URL to get video from. Will also check the URL
        is a valid YT video link.
        """
        self.__YTV = PYT(URL)
        try:
            self.__YTV.streams
            return self.__YTV.title
        except exception as e:
            ### Throw an exception here if the URL is invalid
            raise e

    def get_streams_raw(self):
        """
        Returns the streams for the associated YTV object.
        Unprocessed and raw full data returned by this method.
        """
        return self.__YTV.streams

    def get_streams(self) -> list:
        """
        Returns a list of YTVid's containing necessary info for each
        stream
        """
        YTStreams = []
        for stream in self.__YTV.streams:
            vid = YTVid()
            vid.tag = stream.itag
            vid.mime_type = stream.mime_type
            vid.bitrate = stream.bitrate
            vid.audio_codec = stream.video_codec
            vid.video_codec = stream.audio_codec
            vid.avtype = stream.type
            if stream.resolution != None:
                # Strip the p from the resolution and cast to an integer
                vid.resolution = int(stream.resolution[:-1])
            vid.is_progressive = not stream.is_dash
            vid.filesize = stream._filesize
            YTStreams.append(vid)
        return YTStreams

    def add_download_progress_callback(self, callback):
        """
        Add a callback function that will be called whenever donwload progress
        is made
        func: Callable[[Any, bytes, int], None]
        """
        self.__YTV.register_on_progress_callback(callback)

    def download_stream(self, ytvid: YTVid, download_directory="", filename="") -> str:
            """
            The actual download function that downloads the actual stream into a file.
            Returns: OS path filename of the downloaded stream
            """
            # Use current directory if the download directory is blank
            if download_directory == "":
                download_directory = os.getcwd()
            # Use video title if filename is blank
            if filename == "":
                filename = self.__YTV.title

            # Perform the actual download function
            try:
                file_path = self.__YTV.streams.get_by_itag(ytvid.tag).download(output_path= download_directory, filename= filename, filename_prefix= 'tmp__')
            except Exception as e:
                print(f"Download Error {e}")
                file_path = ""
                raise
            return file_path
        