import os

def get_ak():
    s = os.getenv("VOLC_ACCESSKEY")
    if (s is None):
        s = os.getenv("VOLC_ACCESS_KEY_ID")
    return s

def get_sk():
    s = os.getenv("VOLC_SECRETKEY")
    if (s is None):
        s = os.getenv("VOLC_ACCESS_KEY_SECRET")
    return s
