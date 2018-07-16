from functools import partial
from luigi.contrib.mongodb import MongoCellTarget

from setup import config, mongo


ConnectedMongoCellTarget = partial(
    MongoCellTarget,
    mongo_client=mongo,
    index=config['mongo']['index'],
)
