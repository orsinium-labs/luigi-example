import pymongo
from luigi.configuration import get_config


config = get_config()


mongo = pymongo.MongoClient(
    host=config['mongo']['host'],
    port=config['mongo']['port'],
)
