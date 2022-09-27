import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class VideoEdit:

    def sub_clip(self, video, start, end, output, to_full_duration=False):
        if to_full_duration:
            duration = self.clip_duration(video)
            interval = end - start
            index = 0
            sub_clip_file_name_list = []
            while start <= duration:
                output_file_name = r"{0}_{1}".format(index, output)
                ffmpeg_extract_subclip(r"{}".format(video), start, start + interval,
                                       targetname=output_file_name)
                sub_clip_file_name_list.append(output_file_name)
                start += interval
                index += 1
            return sub_clip_file_name_list
        else:
            return ffmpeg_extract_subclip(video, start, end, targetname=output)

    def extract_audio(self, video, output):
        clip = mp.VideoFileClip(r"{}".format(video))
        clip.audio.write_audiofile(r"{}".format(output), verbose=False, logger=None)

    def clip_duration(self, video):
        return mp.VideoFileClip(r"{}".format(video)).duration
