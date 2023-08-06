import json


class DataReader(object):
    def __init__(self):
        pass

    def read_as_columns(self, path):
        data = {}
        metadata = {}

        with open(path) as f:
            for line in f:
                ex = json.loads(line)
                for k, v in ex.items():
                    data.setdefault(k, []).append(v)

        dataset = {}
        dataset['data'] = data
        dataset['metadata'] = metadata

        return dataset

    def read_as_rows(self, path):
        data = {}
        metadata = {}

        with open(path) as f:
            for line in f:
                ex = json.loads(line)
                data.setdefault('examples', []).append(ex)

        dataset = {}
        dataset['data'] = data
        dataset['metadata'] = metadata

        return dataset
