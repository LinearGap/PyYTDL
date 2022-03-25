import argparse
from ast import arg

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
        self.__settings['resolution'] = args.r
        self.__settings['open'] = args.p
        self.__YTURL = args.url

    def __check_url(self):
        """
        Check the supplied URL is a valid URL. Remove the video identifier and append back to
        YouTube link to ensure safety.
        """
        pass

# ----------------------------------------------------------------------------------
def main():
    ytdl = PyYTDL()

if __name__ == '__main__':
    main()