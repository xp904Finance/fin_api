import base64
import uuid


def new_token():
    return base64.b64encode(uuid.uuid4().hex.encode('utf-8')).decode('utf-8')