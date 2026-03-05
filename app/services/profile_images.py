"""
Profile image helpers for per-profile images.
"""
import os
from flask import current_app

PROFILE_IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.webp')


def _profile_image_dir(root_path=None):
    base = root_path or current_app.root_path
    return os.path.join(base, 'static', 'uploads', 'profile_images')


def get_profile_image_url(profile_name, root_path=None):
    image_dir = _profile_image_dir(root_path)
    if not os.path.isdir(image_dir):
        return None
    for ext in PROFILE_IMAGE_EXTS:
        filename = f"{profile_name}{ext}"
        filepath = os.path.join(image_dir, filename)
        if os.path.isfile(filepath):
            return f"/static/uploads/profile_images/{filename}"
    return None


def clear_profile_image(profile_name, root_path=None):
    image_dir = _profile_image_dir(root_path)
    if not os.path.isdir(image_dir):
        return
    for ext in PROFILE_IMAGE_EXTS:
        filepath = os.path.join(image_dir, f"{profile_name}{ext}")
        if os.path.isfile(filepath):
            os.remove(filepath)
