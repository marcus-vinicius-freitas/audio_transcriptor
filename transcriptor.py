import speech_recognition as sr
from os import path
from pydub import AudioSegment
from pprint import pprint

import config


class Transcriptor:

    def transcribe(self, file, language, output):
        # transcribe audio file
        try:
            sound = AudioSegment.from_mp3(file)
            sound.export(config.AUDIO_WAVE_FILE, format="wav")

            audio_file = path.join(path.dirname(path.realpath(__file__)), config.AUDIO_WAVE_FILE)

            r = sr.Recognizer()
            with sr.AudioFile(audio_file) as source:
                audio = r.record(source)
            text = r.recognize_google(audio, key=config.API_KEY, language=language, show_all=False)
            if output:
                with open(output, 'w') as f:
                    pprint(text, width=120, stream=f)
            else:
                pprint(text, width=120)
        except sr.UnknownValueError:
            pprint("Could not understand audio")
        except sr.RequestError as e:
            pprint("Could not request results from Speech Recognition service; {0}".format(e))
