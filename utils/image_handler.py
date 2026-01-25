from datetime import datetime


def post_image_upload_path(instance, filename):
    """
    產生路徑格式：post_images/YYYY/MM/slug/filename
    """
    now = datetime.now()

    # 預設 slug
    slug = "uncategorized"

    if instance.post:
        slug = instance.post.slug
    elif hasattr(instance, "temp_slug") and instance.temp_slug:
        slug = instance.temp_slug

    # 組合路徑
    return f"post_images/{now.year}/{now.month:02d}/{slug}/{filename}"
