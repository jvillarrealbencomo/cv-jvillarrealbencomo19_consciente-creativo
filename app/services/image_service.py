"""
Image upload and thumbnail service for credential images.
Stores files under app/static/uploads/<category>/ and returns relative paths
usable with url_for('static', filename=... ).
"""
import os
from datetime import datetime
from typing import Optional, Dict
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


class ImageService:
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    THUMBNAIL_SIZE = (200, 200)

    @staticmethod
    def _allowed_file(filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ImageService.ALLOWED_EXTENSIONS

    @staticmethod
    def save_credential_image(file_storage, category: str, record_id: int) -> Optional[Dict[str, str]]:
        """Save uploaded credential image and generate thumbnail if applicable.

        Returns a dict with relative paths (from static/) for image and thumbnail.
        """
        if not file_storage or file_storage.filename == "":
            return None

        if not ImageService._allowed_file(file_storage.filename):
            raise ValueError("Invalid file type. Allowed: png, jpg, jpeg, pdf")

        # Enforce size limit
        file_storage.stream.seek(0, os.SEEK_END)
        file_size = file_storage.stream.tell()
        file_storage.stream.seek(0)
        if file_size > ImageService.MAX_FILE_SIZE:
            raise ValueError("File too large. Max size is 5MB")

        # Prepare paths
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = secure_filename(file_storage.filename)
        ext = original_name.rsplit(".", 1)[1].lower()
        new_filename = f"{category}_{record_id}_{ts}.{ext}"
        static_root = current_app.static_folder
        upload_dir = os.path.join(static_root, "uploads", category)
        os.makedirs(upload_dir, exist_ok=True)
        abs_path = os.path.join(upload_dir, new_filename)

        # Save original
        file_storage.save(abs_path)

        # Build relative path used by url_for('static', filename=rel_path)
        rel_path = os.path.join("uploads", category, new_filename).replace("\\", "/")

        # Generate thumbnail only for images
        thumb_rel = None
        if ext in {"png", "jpg", "jpeg"}:
            thumb_name = f"{category}_{record_id}_{ts}_thumb.jpg"
            thumb_abs = os.path.join(upload_dir, thumb_name)
            with Image.open(abs_path) as img:
                img.thumbnail(ImageService.THUMBNAIL_SIZE)
                img.convert("RGB").save(thumb_abs, "JPEG", quality=85)
            thumb_rel = os.path.join("uploads", category, thumb_name).replace("\\", "/")

        return {
            "image_path": rel_path,
            "thumbnail_path": thumb_rel,
            "filename": original_name,
            "mime_type": file_storage.mimetype,
        }

    @staticmethod
    def delete_credential_image(rel_path: Optional[str], thumb_rel_path: Optional[str] = None) -> None:
        """Delete stored credential image and thumbnail (safe if missing)."""
        static_root = current_app.static_folder
        for rel in [rel_path, thumb_rel_path]:
            if not rel:
                continue
            abs_path = os.path.join(static_root, rel)
            try:
                if os.path.exists(abs_path):
                    os.remove(abs_path)
            except Exception:
                # Do not raise; best-effort cleanup
                pass
