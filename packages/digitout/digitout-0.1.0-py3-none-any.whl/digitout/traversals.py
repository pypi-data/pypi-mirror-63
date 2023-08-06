import sys
import itertools
from inspect import isfunction, ismethod, isclass, isgeneratorfunction, signature, Parameter
from math import inf
from .matchers import ValueMatcher, AttrMatcher, IterMatcher, ItemMatcher, CallMatcher
from .utils import ismapping, isiterable

class ExploreError(Exception):
    def __init__(self, exc):
        self.exc = exc

class Traversal:
    """Traverse certain kind of edges while firing machers on the way.

    Horizontal traversals are preferred.
    """

    def __init__(self, settings, context, reporter):
        self._context = context
        self._reporter = reporter
        self._set_up(settings)

    def _set_up(self, settings):
        pass

    def set_limits(self, max_depth, **kwargs):
        self._max_depth = max_depth

    def set_traversals(self, traversals):
        self._traversals = traversals

    def set_matchers(self, matchers):
        raise NotImplemented

    def inspect(self, path, depth, entry):
        """Traverse starting from entry.

        Args:
            path: str, Expression that evaluates to entry.
            depth: int, Maxmal denivelation.

        Yields:
            NoneType: traversal should yield None to indicate that another traversal should be switched to.
        """
        raise NotImplemented

class ValueTraversal(Traversal):
    """Do not actually . Only fire machers on current node."""

    def set_matchers(self, matchers):
        self._matchers = [matcher for matcher in matchers if isinstance(matcher, ValueMatcher)]

    def inspect(self, path, depth, entry):

        for matcher in self._matchers:
            matcher.check(path, value=entry)

        yield from ()

class IterTraversal(Traversal):

    def _set_up(self, settings):
        self._inspect = settings.get('inspect', True)
        self._max_count = settings.get('max_count', inf)

    def set_matchers(self, matchers):
        self._matchers = [matcher for matcher in matchers if isinstance(matcher, IterMatcher)]

    def inspect(self, path, depth, entry):

        if not isiterable(entry):
            return

        if depth >= self._max_depth:
            return

        limiter = itertools.count() if self._max_count == inf else range(self._max_count)
        scope = [item_value for item_index, item_value in zip(limiter, entry)]
        path_format = f'list({path})[{{}}]'

        for matcher in self._matchers:
            for item_index, item_value in enumerate(scope):
                matcher.check(path_format.format(item_index), index=item_index, value=item_value)

        if not (self._inspect):
            return

        yield

        depth += 1
        gens = []

        for item_index, item_value in enumerate(scope):
            gens += [traversal.inspect(path_format.format(item_index), depth, item_value) for traversal in self._traversals]

        while gens:
            for gen in gens:
                stopped = next(gen, True)
                if stopped:
                    gens.remove(gen)
            yield

class ItemTraversal(Traversal):

    def _set_up(self, settings):
        self._inspect_values = settings.get('inspect_values', True)
        self._inspect_keys = settings.get('inspect_keys', False)

        iterator_name = settings = settings.get('iterator', 'call_items_method')

        iterators = {}
        iterators['call_items_method'] = (
            lambda obj: obj.items(),
            'list({path}.items())[{item_index}][1]',
            'list({path}.items())[{item_index}][0]',
            )

        iterators['zip_keys_and_values'] = (
            lambda obj: zip(obj.keys(), obj.values()),
            'list({path}.values())[{item_index}]',
            'list({path}.keys())[{item_index}]',
            )

        iterators['subscribe_from_keys'] = (
            lambda obj: ((key, obj[key]) for key in obj.keys()),
            '{path}[{item_key!r}]',
            'list({path}.keys())[{item_index}]',
            )

        if iterator_name not in iterators:
            raise Exception('Invalid iterator name')

        self._iterator, self._get_val_fmt, self._get_key_fmt = iterators[iterator_name]


    def set_matchers(self, matchers):
        self._matchers = [matcher for matcher in matchers if isinstance(matcher, ItemMatcher)]

    def inspect(self, path, depth, entry):

        if not ismapping(entry):
            return

        if depth >= self._max_depth:
            return

        scope = {item_key: (self._get_val_fmt.format(path=path, item_key=item_key, item_value=item_value, item_index=item_index),
                            self._get_key_fmt.format(path=path, item_key=item_key, item_value=item_value, item_index=item_index),
                            item_value)
                 for item_index, (item_key, item_value) in enumerate(self._iterator(entry))}

        for matcher in self._matchers:
            for item_key, (path_val, path_key, item_value) in scope.items():
                matcher.check(path_val, key=item_key, value=item_value)

        if not (self._inspect_values or self._inspect_keys):
            return

        yield

        depth += 1
        gens = []

        for item_key, (path_val, path_key, item_value) in scope.items():
            if self._inspect_values:
                gens += [traversal.inspect(path_val, depth, item_value) for traversal in self._traversals]
            if self._inspect_keys:
                gens += [traversal.inspect(path_key, depth, item_key) for traversal in self._traversals]

        while gens:
            for gen in gens.copy():
                stopped = next(gen, True)
                if stopped:
                    gens.remove(gen)
            yield

class AttrTraversal(Traversal):

    def _set_up(self, settings):
        self._inspect = settings.get('inspect', True)
        self._skip_types = settings.get('skip_types', [])
        self._skip_functions = settings.get('skip_functions', False)
        self._skip_methods = settings.get('skip_methods', False)
        self._skip_private = settings.get('skip_private', False)
        self._skip_dunders = settings.get('skip_dunders', False)

    def set_matchers(self, matchers):
        self._matchers = [matcher for matcher in matchers if isinstance(matcher, AttrMatcher)]

    def _skip_target(self, attr_name, attr_value):

        if isinstance(attr_value, ExploreError):
            return True

        if self._skip_private and attr_name.startswith('_'):
            return True

        if self._skip_dunders and attr_name.startswith('__') and attr_name.endswith('__'):
            return True

        if self._skip_functions and isfunction(attr_value):
            return True

        if self._skip_methods and ismethod(attr_value):
            return True

        if type(attr_value) in self._skip_types:
            return True

    def inspect(self, path, depth, entry):

        if depth >= self._max_depth:
            return
        scope = {}

        for attr_name in dir(entry):
            try:
                attr_value = getattr(entry, attr_name)
            except AttributeError as exc:
                attr_value = ExploreError(exc)

            if not self._skip_target(attr_name, attr_value):
                scope[attr_name] = (f'{path}.{attr_name}', attr_value)

        for attr_name, (path, attr_value) in scope.items():
            for matcher in self._matchers:
                matcher.check(path, name=attr_name, value=attr_value)

        if not (self._inspect):
            return

        yield

        depth += 1
        gens = []

        for attr_name, (path, attr_value) in scope.items():
            gens += [traversal.inspect(path, depth, attr_value) for traversal in self._traversals]
            #if self._traverse_names:
            #    gens += [traversal.inspect(path + '<name>', depth, attr_name) for traversal in self._traversals]

        while gens:
            for gen in gens.copy():
                stopped = next(gen, True)
                if stopped:
                    gens.remove(gen)
            yield

class CallTraversal(Traversal):

    def _set_up(self, settings):
        self._inspect = settings.get('inspect', True)
        self._skip_classes = settings.get('skip_classes', False)
        self._skip_genfunc = settings.get('skip_genfunc', False)
        self._skip_callables = []

        for expression in settings.get('skip_callables', []):
            try:
                obj = eval(expression, self._context, None)
            except Exception as exc:
                self._reporter(f"Error while evaluating {expression!r}: {exc}", file=sys.stderr)
            else:
                self._skip_callables.append(obj)

    def set_matchers(self, matchers):
        self._matchers = [matcher for matcher in matchers if isinstance(matcher, CallMatcher)]

    def _skip_target(self, target):
        if not callable(target):
            return True

        if self._skip_classes and isclass(target):
            return True

        if self._skip_genfunc and isgeneratorfunction(target):
            return True

        try:
            params = signature(target).parameters
        except Exception:
            return True
        else:
            defaults = [param.default for param in params.values() if param.default is not Parameter.empty]
            if len(params) > len(defaults):
                return True

        if target in self._skip_callables:
            return True

    def inspect(self, path, depth, entry):

        if depth >= self._max_depth:
            return

        if not (self._inspect) or self._skip_target(entry):
            return

        yield

        depth += 1
        try:
            return_value = entry()
        except Exception:
            return

        new_path = f'{path}()'
        gens = [traversal.inspect(new_path, depth, return_value) for traversal in self._traversals]

        while gens:
            for gen in gens.copy():
                stopped = next(gen, True)
                if stopped:
                    gens.remove(gen)
            yield
