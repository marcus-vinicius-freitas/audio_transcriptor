import argparse
from pprint import pprint

import config
from transcriptor import Transcriptor
from video_edit import VideoEdit

parser = argparse.ArgumentParser(description='Converts audio files to text')
parser.add_argument('file', help='The audio file to convert')
parser.add_argument('-o', '--output', help='The output file')
parser.add_argument('-l', '--language', help='The language of the audio file')
args = parser.parse_args()

if __name__ == '__main__':

    if args.language:
        language = args.language
    else:
        language = 'en-US'

    print("Transcribing audio file...")
    transcriptor = Transcriptor()
    if args.file.endswith('.mp3'):
        print("transcribing mp3 file...")
        transcriptor.transcribe(args.file, language, args.output)
    elif args.file.endswith('.mp4'):
        print("transcribing mp4 file...")
        video_edit = VideoEdit()
        print("cutting video file...")
        sub_clip_file_name_list = video_edit.sub_clip(args.file, 0, 300, config.SUB_CLIP_OUTPUT_FILE,
                                                      to_full_duration=True)
        if isinstance(sub_clip_file_name_list, list):
            print("sub clips...{0}".format(sub_clip_file_name_list))
            file_index = 0
            for sub_clip_file_name in sub_clip_file_name_list:
                print("extracting audio from {0}".format(sub_clip_file_name))
                video_edit.extract_audio(sub_clip_file_name, r"{0}_{1}".format(
                    file_index, config.SUB_AUDIO_OUTPUT_FILE))
                print("transcribing file {0}".format(sub_clip_file_name))
                file_index += 1
                transcriptor.transcribe(r"{0}_{1}".format(file_index, config.SUB_AUDIO_OUTPUT_FILE), language,
                                        r"{0}_{1}".format(file_index, args.output))
        else:
            print("extracting audio...")
            video_edit.extract_audio(config.SUB_CLIP_OUTPUT_FILE, config.SUB_AUDIO_OUTPUT_FILE)
            print("transcribing...")
            transcriptor.transcribe(config.SUB_AUDIO_OUTPUT_FILE, language, args.output)
            print("Done.")
    else:
        pprint('The file format is not supported')
