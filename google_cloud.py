import os.path
import sys
from datetime import datetime
from pprint import pprint

from google.cloud import speech


class GoogleCloud:
    # noinspection PyTypeChecker
    def __init__(self, language):
        self.client = speech.SpeechClient()
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=2)
        self.config = speech.RecognitionConfig(
            language_code=language,
            enable_word_time_offsets=True,
            diarization_config=diarization_config,
        )

    def transcribe(self, file_url, output):
        audio = speech.RecognitionAudio(uri=file_url)
        response = self.client.long_running_recognize(config=self.config, audio=audio)
        diarization_output = "diarization_{}".format(output)
        if os.path.exists(output):
            os.remove(output)
        for result in response.result().results:
            transcript = result.alternatives[0].transcript
            if transcript:
                with open(output, 'a') as f:
                    f.write(transcript)

        result = response.result().results[-1]
        words_info = result.alternatives[0].words
        with open("log_{}.txt".format(datetime.now().microsecond), "a") as log_file:
            print("words_info: {}".format(words_info), file=log_file)

        current_speaker = -1
        original_stdout = sys.stdout
        words_per_line = 1
        max_words_per_line = 30
        if os.path.exists(diarization_output):
            os.remove(diarization_output)
        with open("diarization_{}".format(output), 'a') as f:
            sys.stdout = f
            for word_info in words_info:
                if word_info.speaker_tag != current_speaker:
                    current_speaker = word_info.speaker_tag
                    print("\n")
                    print("Speaker {}".format(current_speaker))
                    print(word_info.word, end=" ")
                else:
                    if words_per_line <= max_words_per_line:
                        print(word_info.word, end=" ")
                        words_per_line += 1
                    else:
                        print(word_info.word)
                        words_per_line = 1
            print("\n")
        sys.stdout = original_stdout

