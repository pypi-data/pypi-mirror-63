import os
import sys

if __name__ == '__main__':
    os.environ["CONFIG_PATH"] = sys.argv[1]
    os.system('gunicorn -c gunicorn.py ../wsgi:api --reload')
