import argparse

import config
from recognizer import Recognizer

parser = argparse.ArgumentParser(description='Converts audio files to text')
parser.add_argument('file', help='The audio file to convert')
parser.add_argument('-o', '--output', help='The output file')
parser.add_argument('-l', '--language', help='The language of the audio file')
parser.add_argument('-e', '--engine', help='The engine to use for the conversion')
parser.add_argument('-i', '--interval', help='The interval to cut the media file')
args = parser.parse_args()

if __name__ == '__main__':

    if args.language:
        language = args.language
    else:
        language = 'en-US'

    if args.engine:
        engine = args.engine
    else:
        engine = config.GOOGLE

    if args.interval:
        interval = args.interval
    else:
        interval = 60

    print("Transcription started...")
    recognizer = Recognizer()
    recognizer.send_data(file=args.file, language=language, output=args.output, engine=engine, interval=interval)
