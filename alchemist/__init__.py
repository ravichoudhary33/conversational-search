import os
from yaml import load, Loader

dir_path = os.path.dirname(os.path.realpath(__file__))
config_file_path = os.path.join(dir_path, 'config.yaml')
APPLICATION_CONFIG = load(open(config_file_path), Loader=Loader)


REDIS_HOST = os.environ.get("")
STATSD_HOST = os.environ.get("")
STATSD_PORT = os.environ.get("")

#downstream 
RERANKER_HOST = os.environ.get("")
SEARCH_HOST = os.environ.get("")
OPEN_AI_HOST = os.environ.get("")

ALCHEMY_HOST = os.environ.get("")