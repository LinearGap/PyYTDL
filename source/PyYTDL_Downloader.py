from logging import exception
from pytube import YouTube as PYT

class YTVid():
    """
    Object that will contain information about each available stream available
    for the supplied urls
    Tag = Specific identifier for that video stream
    Mime_type = The multimedia type
    Resolution = The resolution of the video
    Bitrate = The video bitrate of the stream
    AVType = What type of stream is this Audio/Video
    Is_Progresive = Is this a progressive type stream that contains audio and video
    Video_codec = What video codec is this stream encoded with
    Audio_codec = What audio codec is this stream encoded with
    Filesize = How big is the full stream
    """
    def __init__(self):
        self.tag = 0
        self.mime_type = ""
        self.resolution = ""
        self.bitrate = ""
        self.avtype = ""
        self.is_progressive = False
        self.video_codec = ""
        self.audio_codec = ""
        self.filesize = 0

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
        is a valid YT video link
        """
        self.__YTV = PYT(URL)
        try:
            self.__YTV.streams
        except:
            print('error')

    def get_streams_raw(self):
        """
        Returns the streams for the associated YTV object.
        Unprocessed and raw full data returned by this method.
        """
        return self.__YTV.streams

    def get_streams(self):
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
            vid.resolution = stream.resolution
            vid.is_progressive = not stream.is_dash
            vid.filesize = stream._filesize
            YTStreams.append(vid)
        return YTStreams