import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class MediaManager:

    def sub_clip(self, source, start, end, output, to_full_duration=False):
        if to_full_duration:
            duration = self.clip_duration(source)
            interval = end - start
            index = 0
            sub_clip_file_name_list = []
            while start <= duration:
                output_file_name = r"{0}_{1}".format(index, output)
                ffmpeg_extract_subclip(r"{}".format(source), start, start + interval,
                                       targetname=output_file_name)
                sub_clip_file_name_list.append(output_file_name)
                start += interval
                index += 1
            return sub_clip_file_name_list
        else:
            return ffmpeg_extract_subclip(source, start, end, targetname=output)

    def extract_audio(self, source, output, codec='mp3', mono=False):
        clip = mp.VideoFileClip(r"{}".format(source))
        audio = clip.audio
        ffmpeg_params = None
        if mono:
            ffmpeg_params = ['-ac', '1']
        audio.write_audiofile(r"{}".format(output), verbose=False, logger=None, codec=codec,
                              ffmpeg_params=ffmpeg_params)

    def clip_duration(self, video):
        return mp.VideoFileClip(r"{}".format(video)).duration
