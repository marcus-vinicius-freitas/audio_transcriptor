import argparse
from Recognizer import Engine, Recognizer

parser = argparse.ArgumentParser(description='Converts audio files to text')
parser.add_argument('file', help='The audio file to convert')
parser.add_argument('-o', '--output', help='The output file')
parser.add_argument('-l', '--language', help='The language of the audio file')
parser.add_argument('-e', '--engine', help='The engine to use for the conversion')
args = parser.parse_args()

if __name__ == '__main__':

    if args.language:
        language = args.language
    else:
        language = 'en-US'

    if args.engine:
        engine = args.engine
    else:
        engine = Engine.GOOGLE

    recognizer = Recognizer()
    recognizer.send_data(args.file, language, args.output, 0, 120, True, engine)
