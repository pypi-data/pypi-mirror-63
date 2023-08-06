from itertools import groupby
from .matchers import TargetNotFound

class SearchEngine:

    def __init__(self, traversals, matchers, settings):

        self._traversals = traversals
        self._setting = settings

        for matcher in matchers:
            matcher.set_up(**settings)

        for traversal in self._traversals:
            traversal.set_traversals(self._traversals)
            traversal.set_matchers(matchers)
            traversal.set_limits(**settings)

    def search(self, entry):
        gens = [traversal.inspect('target', 0, entry) for traversal in self._traversals]
        while gens:
            for gen in gens.copy():
                stopped = next(gen, True)
                if stopped:
                    gens.remove(gen)

        raise TargetNotFound()
