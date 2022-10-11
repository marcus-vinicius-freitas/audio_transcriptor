import sys

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
        for result in response.result().results:
            transcript = result.alternatives[0].transcript
            if transcript:
                with open(output, 'w') as f:
                    f.write(transcript)

        transcript = response.result().results[0].alternatives[0].transcript
        result = response.result().results[-1]
        words_info = result.alternatives[0].words
        used_words_index = [0] * len(words_info)

        original_stdout = sys.stdout
        current_speaker = -1
        words_per_line = 1
        with open("diarization_{}".format(output), 'w') as f:
            sys.stdout = f
            for word in transcript.split():
                word_index = [i for i, j in enumerate(words_info) if j.word == word and used_words_index[i] == 0]
                if len(word_index) > 0:
                    used_words_index[word_index[0]] = 1
                    _word = words_info[word_index[0]]
                    if _word.speaker_tag != current_speaker:
                        current_speaker = _word.speaker_tag
                        print("\n")
                        print("Speaker {}".format(current_speaker))
                        print(_word.word, end=" ")
                    else:
                        if words_per_line <= 20:
                            print(_word.word, end=" ")
                            words_per_line += 1
                        else:
                            print(_word.word)
                            words_per_line = 1
            print("\n")
        sys.stdout = original_stdout

