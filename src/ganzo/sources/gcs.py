import os

from google.cloud import storage

from ganzo.sources import TemplateSource


# Because of Python <=3.8
def _remove_prefix(text: str, prefix: str) -> str:
    return text[len(prefix) :] if text.startswith(prefix) else text


class GCSSource(TemplateSource):
    def __init__(
        self,
        bucket_name: str,
        template_list_file_name: str = "templates.list",
    ):
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.template_list_file_name = template_list_file_name

    def list_templates(self):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(self.template_list_file_name)
        content = blob.download_as_bytes().decode("utf-8")
        return content.strip().split("\n")

    def load_template(self, template_name: str, target_path: str):
        template_path = f"{template_name}/"
        blobs = self.client.list_blobs(self.bucket_name, prefix=template_path)

        empty = True
        for blob in blobs:
            empty = False
            file_relative_path = _remove_prefix(blob.name, template_path)
            file_path = os.path.join(target_path, file_relative_path)
            file_dir, _ = os.path.split(file_path)

            print(f"Loading 'gs://{blob.bucket.name}/{blob.name}' into '{file_path}'")
            os.makedirs(file_dir, exist_ok=True)
            blob.download_to_filename(file_path)

        if empty:
            raise ValueError(f"Template '{template_name}' does not exist.")
