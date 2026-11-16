from pathlib import Path

from django.conf import settings


MEDIA_UPLOAD_PREFIXES = ('products/',)


def _cloudinary_active() -> bool:
    backend = getattr(settings, 'STORAGES', {}).get('default', {}).get('BACKEND', '')
    return backend.endswith('MediaCloudinaryStorage')


def _cloudinary_public_id(file_field) -> str | None:
    name = getattr(file_field, 'name', None)
    if not name or str(name).startswith('http'):
        return None

    raw = str(name).replace('\\', '/').lstrip('/')
    path = Path(raw)
    public_id = path.with_suffix('').as_posix()

    # Fresh product uploads are stored under Cloudinary's "media/products/" folder
    # while Django may keep only "products/..." in the database.
    if (
        not raw.startswith('media/')
        and not path.suffix
        and raw.startswith(MEDIA_UPLOAD_PREFIXES)
    ):
        public_id = f'media/{public_id}'

    return public_id


def _cloudinary_absolute_url(file_field) -> str | None:
    public_id = _cloudinary_public_id(file_field)
    if not public_id:
        return None

    try:
        import cloudinary
    except ImportError:
        return None

    return cloudinary.CloudinaryImage(public_id).build_url(secure=True)


def _absolute_field_url(file_field) -> str | None:
    try:
        url = file_field.url
    except Exception:
        return None
    if url.startswith(('http://', 'https://')):
        return url
    return None


def media_absolute_url(request, file_field):
    """Prefer Cloudinary when configured; otherwise serve on-disk media from API origin."""
    if not file_field:
        return None

    if _cloudinary_active():
        cloud_url = _cloudinary_absolute_url(file_field)
        if cloud_url:
            return cloud_url
        direct_url = _absolute_field_url(file_field)
        if direct_url:
            return direct_url

    name = getattr(file_field, 'name', None)
    if name and not str(name).startswith('http'):
        local = Path(settings.MEDIA_ROOT) / name
        if local.is_file():
            origin = getattr(settings, 'PUBLIC_API_ORIGIN', '').rstrip('/')
            if origin:
                return f'{origin}/media/{name}'

    url = file_field.url
    if url.startswith(('http://', 'https://')):
        return url

    origin = getattr(settings, 'PUBLIC_API_ORIGIN', '').rstrip('/')
    if origin:
        return f'{origin}{url}'
    if request:
        return request.build_absolute_uri(url)
    return url
