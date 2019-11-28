import hashlib


SECRET_KEY = 'aKdk27&ak*901'


def encode4md5(txt):
    md5_ = hashlib.md5(txt.encode('utf-8'))
    md5_.update(SECRET_KEY.encode('utf-8'))

    return md5_.hexdigest()