from decouple import config

SECRET_KEY = config('SECRET_KEY')

# line bot setting

LINE_CHANNEL_ACCESS_TOKEN = config('LINE_CHANNEL_ACCESS_TOKEN')

LINE_CHANNEL_SECRET = config('LINE_CHANNEL_SECRET')

HASH_SECRET = config('HASH_SECRET')

import hashlib
def get_hash(data:str,salt=HASH_SECRET):
    if data:
        m = hashlib.sha256()
        m.update(data.encode())
        m.update(salt.encode())
        return m.hexdigest()
    return data
    