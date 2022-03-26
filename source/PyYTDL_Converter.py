import ffmpeg
class PyYTDL_Converter():
    """
    Class that handles converting videos from the formats downloaded
    from YouTube and into something more useable and relevant
    """
    def __init__(self):
        #Audio and Video inputs
        self.__v_input = None
        self.__a_input = None

        #Output object
        self.__output_obj = None

    def set_video_input(self, video_filename):
        """
        Set the video input for conversion and store
        """
        try:
            v_in = ffmpeg.input(video_filename)
            v_s = v_in.video

            self.__v_input = v_s
        except:
            raise

    def set_audio_input(self, audio_filename):
        """
        Set the audio input for conversion and store
        """
        try:
            a_in = ffmpeg.input(audio_filename)
            a_s = a_in.audio

            self.__a_input = a_s
        except:
            raise

    def set_output_file(self, audio_only, output_name_and_ext):
        """
        Setup the output object using input streams and specified
        output names
        """
        ff_out = None
        try:
            if audio_only:
                ff_out = ffmpeg.output(self.__a_input, output_name_and_ext, acodec='aac')
            else:
                ff_out = ffmpeg.output(self.__v_input, self.__a_input, output_name_and_ext, vcodec='libx264', acodec='aac')
        except:
            raise

        self.__output_obj = ff_out

    def convert(self, quiet=True):
        """
        Run the actual conversion. If quiet specified then hide outputs
        """
        pipe = self.__output_obj.run(quiet=quiet, overwrite_output=True, capture_stdout=True)

