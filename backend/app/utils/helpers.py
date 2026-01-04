from flask import current_app
import os
import uuid


def allowed_file(filename: str) -> bool:
    """Return True if filename has an allowed extension configured in app."""
    if not filename:
        return False
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config.get('ALLOWED_EXTENSIONS', set())


def save_upload_file(file_storage, subdir: str = 'avatars') -> str:
    """保存上传的文件到指定目录并返回URL路径。

    返回值为相对URL路径，如 /static/uploads/avatars/xxx.jpg
    """
    if file_storage is None:
        return ''

    ext = file_storage.filename.rsplit('.', 1)[1].lower() if '.' in file_storage.filename else ''
    filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex

    upload_folder = current_app.config.get('UPLOAD_FOLDER')
    target_dir = os.path.join(upload_folder, subdir)
    os.makedirs(target_dir, exist_ok=True)

    file_path = os.path.join(target_dir, filename)
    file_storage.save(file_path)

    # 返回URL路径
    return f'/static/uploads/{subdir}/{filename}'
