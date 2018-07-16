from time import sleep
from datetime import date

import luigi

from targets import ConnectedMongoCellTarget
from setup import config


class GenerateTask(luigi.Task):
    num = luigi.IntParameter()

    def run(self):
        sleep(1)
        self.output().write('v{}'.format(self.num))

    def output(self):
        return ConnectedMongoCellTarget(
            collection=config['mongo']['collection'],
            document_id='hello_{}'.format(self.num),
            path='value',
        )


class ConcatenateTask(luigi.Task):
    date = luigi.DateParameter(default=date.today())

    def requires(self):
        for i in range(5):
            yield GenerateTask(i + 1)

    def run(self):
        sleep(1)
        values = []
        for target in self.input():
            values.append(target.read())
        with self.output().open('w') as f:
            f.write(' '.join(values))

    def output(self):
        return luigi.LocalTarget('output_{}.txt'.format(self.date))


TAIL = ConcatenateTask
