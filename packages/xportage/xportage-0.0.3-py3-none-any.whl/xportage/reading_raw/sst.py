import nltk

from xportage.reading_raw.reader import DataReader
import xportage.utils.tree as tree_utils


class SST(DataReader):
    def read(self, path):
        data = {}
        metadata = {}

        with open(path) as f:
            sofar = 0
            for line in f:
                old_line = line[:]
                line = line.replace(' 1\/2', '-1\/2')
                if line != old_line:
                    print('Warning: Changes made to data.')
                    print('Before: {}'.format(old_line.strip()))
                    print(' After: {}'.format(line.strip()))
                tr = nltk.Tree.fromstring(line.strip())
                words = tr.leaves()
                spans = tree_utils.tree_to_spans_for_nltk(tr)

                data.setdefault('example_id', []).append(sofar)
                data.setdefault('sentence', []).append(words)
                data.setdefault('labeled_spans', []).append(spans)

                sofar += 1

        dataset = {}
        dataset['data'] = data
        dataset['metadata'] = metadata

        return dataset
