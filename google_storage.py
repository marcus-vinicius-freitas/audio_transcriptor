from google.cloud import storage

import config


class GoogleStorage:

    def __init__(self):
        self.bucket_name = config.BUCKET_NAME
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(self.bucket_name)

    def upload_file(self, file_name):
        blob = self.bucket.blob(file_name)
        blob.upload_from_filename(file_name)
        print("file uploaded to google storage...{}".format(file_name))

    def get_file_uri(self, file_name):
        blob = self.bucket.blob(file_name)
        return blob.public_url

    def delete_file(self, file_name):
        blob = self.bucket.blob(file_name)
        blob.delete()
        print("file deleted from google storage...{}".format(file_name))
