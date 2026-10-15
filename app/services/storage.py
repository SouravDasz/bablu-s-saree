from __future__ import annotations

import mimetypes
import uuid
from pathlib import PurePosixPath

from supabase import Client, create_client

from app.core.config import SUPABASE_BUCKET, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_URL


def _client() -> Client:
    if not SUPABASE_URL:
        raise RuntimeError("SUPABASE_URL is not configured.")
    if not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not configured.")
    if "publishable" in SUPABASE_SERVICE_ROLE_KEY.lower():
        raise RuntimeError(
            "SUPABASE_SERVICE_ROLE_KEY must contain a Supabase secret/service-role key, "
            "not a publishable key."
        )
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def upload_product_image(file_obj, original_filename: str | None) -> str:
    extension = PurePosixPath(original_filename or "").suffix.lower()
    filename = f"{uuid.uuid4()}{extension}"
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    content = file_obj.read()
    _client().storage.from_(SUPABASE_BUCKET).upload(
        filename,
        content,
        {"content-type": content_type, "upsert": "false"},
    )
    return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"


def delete_product_image(image_url: str | None) -> None:
    if not image_url or not SUPABASE_URL:
        return
    prefix = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/"
    if image_url.startswith(prefix):
        _client().storage.from_(SUPABASE_BUCKET).remove(
            [image_url.removeprefix(prefix)]
        )


def image_url(image: str | None) -> str:
    if not image:
        return ""
    if image.startswith(("http://", "https://")):
        return image
    return f"/files/products/{image}"
