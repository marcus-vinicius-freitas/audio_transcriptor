from google.cloud import speech


class GoogleCloud:
    def __init__(self, language):
        self.client = speech.SpeechClient()
        self.config = speech.RecognitionConfig(
            sample_rate_hertz=16000,
            language_code=language,
        )

    def transcribe(self, file_url):
        audio = speech.RecognitionAudio(uri=file_url)
        response = self.client.long_running_recognize(config=self.config, audio=audio)
        for result in response.result().results:
            print(u"Transcript: {}".format(result.alternatives[0].transcript))
