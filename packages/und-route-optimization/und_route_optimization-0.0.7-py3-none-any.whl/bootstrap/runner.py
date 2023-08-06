import os
import sys

def main():
    os.environ["CONFIG_PATH"] = sys.argv[1]
    os.system('gunicorn bootstrap.wsgi:api --reload -b :8000 -w 2 --timeout 60')
