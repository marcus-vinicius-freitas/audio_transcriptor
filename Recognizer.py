from enum import Enum

import config
from Result import Result
from transcriptor import Transcriptor
from video_edit import VideoEdit


class Engine(Enum):
    GOOGLE = "google"
    GOOGLE_CLOUD = "google_cloud"


class Recognizer:

    def send_data(self, file, language, output, start, end, to_full_duration, engine):
        get_recognizer(file, language, output, start, end, to_full_duration, engine)


def get_recognizer(file, language, output, start, end, to_full_duration, engine):
    if engine == Engine.GOOGLE:
        return _google_recognizer(file, language, output, start, end, to_full_duration)
    elif engine == Engine.GOOGLE_CLOUD:
        # return _google_cloud_recognizer()
        pass


def _google_recognizer(file, language, output, start, end, to_full_duration):
    print("Transcribing audio file...")
    transcriptor = Transcriptor()
    if file.endswith('.mp3'):
        print("transcribing mp3 file...")
        transcriptor.transcribe(file, language, output)
    elif file.endswith('.mp4'):
        print("transcribing mp4 file...")
        video_edit = VideoEdit()
        print("cutting video file...")
        sub_clip_file_name_list = video_edit.sub_clip(file, start, end, config.SUB_CLIP_OUTPUT_FILE,
                                                      to_full_duration=to_full_duration)
        if isinstance(sub_clip_file_name_list, list):
            print("sub clips...{0}".format(sub_clip_file_name_list))
            file_index = 0
            for sub_clip_file_name in sub_clip_file_name_list:
                print("extracting audio from {0}".format(sub_clip_file_name))
                video_edit.extract_audio(sub_clip_file_name, r"{0}_{1}".format(
                    file_index, config.SUB_AUDIO_OUTPUT_FILE))
                print("transcribing file {0}".format(sub_clip_file_name))
                transcriptor.transcribe(r"{0}_{1}".format(file_index, config.SUB_AUDIO_OUTPUT_FILE), language,
                                        r"{0}_{1}".format(file_index, output))
                file_index += 1
        else:
            print("extracting audio...")
            video_edit.extract_audio(config.SUB_CLIP_OUTPUT_FILE, config.SUB_AUDIO_OUTPUT_FILE)
            print("transcribing...")
            transcriptor.transcribe(config.SUB_AUDIO_OUTPUT_FILE, language, output)

        result = Result()
        print("creating output file...")
        result.create_result(sub_clip_file_name_list, output)
        print("Done.")
    else:
        print('The file format is not supported')
