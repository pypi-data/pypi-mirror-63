import json
import nltk


def tree_to_spans_for_nltk(tree):
    spans = []
    def helper(tr, pos=0, depth=0):
        if len(tr) == 1 and isinstance(tr[0], str):
            label = tr.label()
            size = 1
            spans.append((pos, size, label, depth))
            return size
        if len(tr) == 1:
            label = tr.label()
            size = helper(tr[0], pos, depth=depth+1)
            spans.append((pos, size, label, depth))
            return size
        size = 0
        for x in tr:
            xsize = helper(x, pos+size, depth=depth+1)
            size += xsize
        label = tr.label()
        spans.append((pos, size, label, depth))
        return size
    _ = helper(tree)
    return spans
