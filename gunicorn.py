from os import getenv
from dotenv import load_dotenv

load_dotenv() 

print(getenv('LISTEN_PORT'))
# The IP address (typically localhost) and port that the Netbox WSGI process should listen on
bind = '{}:{}'.format(getenv('LISTEN_ADDRESS','0.0.0.0'), getenv('LISTEN_PORT','8080'))

# Number of gunicorn workers to spawn. This should typically be 2n+1, where
# n is the number of CPU cores present.
workers = int(getenv('WORKERS','2'))
