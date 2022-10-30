import requests as r
from celery import shared_task
from django.conf import settings
import uuid

CAT_URL = "http://thecatapi.com/api/images/get?format=src&type=gif"


@shared_task
def report():
    resp = r.get(CAT_URL)
    file_ext = resp.headers.get('Content-Type').split('/')[1]
    file_name = settings.BASE_DIR / 'reports' / (str(uuid.uuid4())+ "." + file_ext)
    with open(file_name, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=128):
            f.write(chunk)
    return True
