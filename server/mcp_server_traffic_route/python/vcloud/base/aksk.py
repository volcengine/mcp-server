import os

def get_ak():
    s = os.getenv("VOLCENGINE_ACCESS_KEY")
    if (s is None):
        s = os.getenv("VOLC_ACCESS_KEY_ID")
    return s

def get_sk():
    s = os.getenv("VOLCENGINE_SECRET_KEY")
    if (s is None):
        s = os.getenv("VOLC_ACCESS_KEY_SECRET")
    return s
