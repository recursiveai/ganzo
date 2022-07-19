import os

from google.cloud import storage


class GCSSource:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket_name = bucket_name

    def list_templates(self):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob("templates.list")
        content = blob.download_as_bytes().decode("utf-8").strip()
        return content.split("\n")

    def load_template(self, template_name: str, target_path: str):
        template_path = f"{template_name}/"
        blobs = self.client.list_blobs(self.bucket_name, prefix=template_path)

        empty = True
        for blob in blobs:
            empty = False
            file_relative_path = blob.name.removeprefix(template_path)
            file_path = os.path.join(target_path, file_relative_path)
            file_dir, _ = os.path.split(file_path)
            print(f"Loading 'gs://{blob.bucket.name}/{blob.name}' into '{file_path}'")
            os.makedirs(file_dir, exist_ok=True)
            blob.download_to_filename(file_path)

        if empty:
            raise ValueError(f"Template '{template_name}' does not exist.")
