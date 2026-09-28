from django.core.files.storage import FileSystemStorage

from .image_utils import compress_image_content


class CKEditorCompressingStorage(FileSystemStorage):
    """Storage backend that compresses CKEditor image uploads automatically."""

    def _save(self, name, content):
        compressed_content = compress_image_content(content)
        return super()._save(name, compressed_content)
