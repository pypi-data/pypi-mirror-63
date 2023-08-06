import os
import sys

def main():
    os.environ["CONFIG_PATH"] = sys.argv[1]
    os.system('gunicorn -c gunicorn.py wsgi:api --reload')
