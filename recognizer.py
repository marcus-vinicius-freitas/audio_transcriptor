import config
from Result import Result
from google_storage import GoogleStorage
from transcriptor import Transcriptor
from media_manager import MediaManager


class Recognizer:

    def send_data(self, file, language, output, engine, interval):
        send_data_to_recognizer(file, language, output, engine, interval)


def send_data_to_recognizer(file, language, output, engine, interval):
    if engine == config.GOOGLE:
        print("engine...{}".format(config.GOOGLE))
        _google_recognizer(file, language, output, 0, interval, True)
    elif engine == config.GOOGLE_CLOUD:
        print("engine...{}".format(config.GOOGLE_CLOUD))
        _google_cloud_recognizer(file, language, output)
    else:
        print("invalid engine...{}".format(engine))


def _google_recognizer(file, language, output, start, end, to_full_duration):
    print("transcribing audio file...")
    transcriptor = Transcriptor()
    if file.endswith('.mp3'):
        print("transcribing mp3 file...")
        transcriptor.transcribe(file, language, output)
    elif file.endswith('.mp4'):
        print("transcribing mp4 file...")
        video_edit = MediaManager()
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


def _google_cloud_recognizer(file, language, output):
    print("transcribing audio file...")
    google_storage = GoogleStorage()
    if file.endswith('.mp3'):
        print("uploading mp3 file...")
        google_storage.upload_file(file)
        file_uri = google_storage.get_file_uri(file)
        print("file uri...{}".format(file_uri))
        print("delete file...")
        google_storage.delete_file(file)
    elif file.endswith('.mp4'):
        print("transcribing mp4 file...")
        video_edit = MediaManager()
        print("extracting audio...")
        video_edit.extract_audio(file, config.SUB_AUDIO_OUTPUT_FILE_WAVE, codec="pcm_s16le")
        print("uploading audio file...")
        google_storage.upload_file(config.SUB_AUDIO_OUTPUT_FILE_WAVE)
        file_uri = google_storage.get_file_uri(file)
        print("file uri...{}".format(file_uri))
        google_storage.delete_file(file)


