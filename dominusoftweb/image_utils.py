import io
import os

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def compress_image_content(
    content,
    *,
    max_width=1920,
    max_height=1920,
    jpeg_quality=80,
    webp_quality=80,
):
    """Compress uploaded image content while preserving a web-friendly format."""
    name = getattr(content, "name", "upload")
    extension = os.path.splitext(name)[1].lower()

    if extension not in SUPPORTED_EXTENSIONS:
        return content

    original_position = None
    if hasattr(content, "tell"):
        try:
            original_position = content.tell()
        except Exception:
            original_position = None

    if hasattr(content, "seek"):
        try:
            content.seek(0)
        except Exception:
            pass

    def _restore_and_return_original():
        if hasattr(content, "seek"):
            try:
                content.seek(0)
            except Exception:
                pass
        return content

    try:
        image = Image.open(content)
        image = ImageOps.exif_transpose(image)
    except Exception:
        return _restore_and_return_original()

    if image.mode == "RGBA" and extension in {".jpg", ".jpeg"}:
        # JPEG does not support alpha channel.
        image = image.convert("RGB")
    elif image.mode not in {"RGB", "RGBA"} and extension in {".jpg", ".jpeg", ".webp"}:
        image = image.convert("RGB")

    image.thumbnail((max_width, max_height), Image.LANCZOS)

    output = io.BytesIO()

    try:
        if extension in {".jpg", ".jpeg"}:
            image.save(output, format="JPEG", optimize=True, quality=jpeg_quality, progressive=True)
        elif extension == ".png":
            image.save(output, format="PNG", optimize=True, compress_level=9)
        elif extension == ".webp":
            image.save(output, format="WEBP", optimize=True, quality=webp_quality, method=6)
        else:
            return _restore_and_return_original()
    except Exception:
        # If encoder support is unavailable (e.g., WEBP), do not block upload.
        return _restore_and_return_original()

    output.seek(0)
    compressed = ContentFile(output.read())
    compressed.name = name
    return compressed
