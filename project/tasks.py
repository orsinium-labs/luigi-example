from time import sleep
from datetime import date

import luigi

from targets import ConnectedMongoCellTarget
from setup import config


class GenerateTask(luigi.Task):
    num = luigi.IntParameter()

    def input(self):
        return ConnectedMongoCellTarget(
            collection=config['mongo']['collection'],
            document_id='hello_{}'.format(self.num),
            path='value',
        )

    def run(self):
        sleep(1)
        self.input().write('v{}'.format(self.num))

    def output(self):
        return luigi.LocalTarget('/tmp/bar/%d' % self.num)


class ConcatenateTask(luigi.Task):
    date = luigi.DateParameter(default=date.today())

    def requires(self):
        for i in range(5):
            yield GenerateTask(i + 1)

    def run(self):
        sleep(1)
        values = []
        for value in self.input():
            values.append(value)
        self.output().write(' '.join(values))

    def output(self):
        return luigi.LocalTarget('output_{}.txt'.format(self.date))


TAIL = ConcatenateTask
