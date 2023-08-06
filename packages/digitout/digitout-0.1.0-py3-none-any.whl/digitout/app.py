import od
import sys
import toml
import colorama
from math import inf
from .traversals import ValueTraversal, ItemTraversal, IterTraversal, AttrTraversal, CallTraversal
from .matchers import ValueMatcher, ItemMatcher, IterMatcher, AttrMatcher, CallMatcher
from .matchers import TargetFound, TargetNotFound
from .engine import SearchEngine
from .tui import open_tui
from .config import load_config, get_from_config, DEFAULT_CONFIG
from typing import Any, Union, Tuple

def interactive_target_found_callback(path, match):
    while True:
        ans = input(f'Match found. Continue? [Y/n]: ').lower()
        if ans == 'y' or ans == '':
            break
        if ans == 'n':
            raise TargetFound(path, match)

def immediate_target_found_callback(path, match):
    raise TargetFound(path, match)

def dummy_target_found_callback(path, match):
    pass

class DigItOut:

    def __init__(self, config, findall, interactive, verbose, context=None):
        colorama.init()
        traversal_list = []
        matcher_list = []

        match_config = get_from_config(config, 'match')
        traversal_config = get_from_config(config, 'traversal')
        expression = get_from_config(config, 'match.expression')
        target = get_from_config(config, 'match.target')
        if target not in ['value', 'item', 'iter', 'attr']:
            raise Exception(f'Incorrect target: {target}')

        match_func = eval(expression, context, None)

        if findall:
            if interactive:
                target_found_callback = interactive_target_found_callback
            else:
                target_found_callback = dummy_target_found_callback
        else:
            target_found_callback = immediate_target_found_callback

        if verbose:
            self.reporter = print
        else:
            self.reporter = lambda *args, **kwargs: None

        value_match_enabled = target == 'value'
        if value_match_enabled:
            traversal_list.append(ValueTraversal(settings={}, context=context, reporter=self.reporter))
            matcher_list.append(ValueMatcher(match_func, self.reporter, target_found_callback))

        item_traversal_config = traversal_config.get('item', {})
        item_match_enabled = target == 'item'
        if item_match_enabled or item_traversal_config.get('inspect_values', False) or item_traversal_config.get('inspect_keys', False):
            traversal_list.append(ItemTraversal(settings=item_traversal_config, context=context, reporter=self.reporter))
            if item_match_enabled:
                matcher_list.append(ItemMatcher(match_func, self.reporter, target_found_callback))

        iter_traversal_config = traversal_config.get('iter', {})
        iter_match_enabled = target == 'iter'
        if iter_match_enabled or iter_traversal_config.get('inspect', False):
            traversal_list.append(IterTraversal(settings=iter_traversal_config, context=context, reporter=self.reporter))
            if iter_match_enabled:
                matcher_list.append(IterMatcher(match_func, self.reporter, target_found_callback))

        attr_traversal_config = traversal_config.get('attr', {})
        attr_match_enabled = target == 'attr'
        if attr_match_enabled or attr_traversal_config.get('inspect', False):
            traversal_list.append(AttrTraversal(settings=attr_traversal_config, context=context, reporter=self.reporter))
            if attr_match_enabled:
                matcher_list.append(AttrMatcher(match_func, self.reporter, target_found_callback))

        call_traversal_config = traversal_config.get('call', {})
        if call_traversal_config.get('inspect', False):
            traversal_list.append(CallTraversal(settings=call_traversal_config, context=context, reporter=self.reporter))
            if attr_match_enabled:
                matcher_list.append(CallMatcher(match_func, self.reporter, target_found_callback))

        engine_settings = get_from_config(config, 'engine')
        engine_settings_coerced = {}
        engine_settings_coerced['stringifier'] = eval('lambda obj: ' + engine_settings.get('stringifier', 'repr(obj)') , context, None)
        engine_settings_coerced['max_check_count'] = engine_settings.get('max_check_count', inf)
        engine_settings_coerced['max_depth'] = engine_settings.get('max_depth', inf)

        self._engine = SearchEngine(traversal_list, matcher_list, engine_settings_coerced)

    def search(self, entry):

        try:
            self._engine.search(entry)
        except TargetFound as exc:
            self.reporter(exc, file=sys.stderr)
            result = exc.path, exc.match
        except TargetNotFound as exc:
            self.reporter(exc, file=sys.stderr)
            result = None, None
        except KeyboardInterrupt:
            result = None, None


        return result


def digitout_verbose(target: Any,
                     config: Union[type(None), str, dict] =None,
                     context: Union[type(None), dict] =None) -> Tuple[str, dict]:
    """
    Traverses through the Python structures until constraint defined in the
    config is met. This function is designed for finding path to the objects
    that you don't know how to get to.

    This function can be called by calling `digitout` module itself. E.g.

    ```python
    import digitout
    digitout(foobar)
    ```

    Arguments:
        target: Top-level object where searching should start from.
        config: `None` - Open TUI if TTY available, or load default config otherwise.
                `str` instance - name of the config to get loaded.
                `dict` instance - config given explicitly.
        context: Variables that should be accessible to the lambda expressions
          defined in the config. Usually `locals()` is passed.

    Returns:
        `(path, match)` pair, where `path` - expressions that evaluates to the
          match, or `None` if match not found. `match` - `dict` of the keys
          which are args of the *Target Constraint* and values corresponding
          the the match, or `None` if match not found.
    """
    if config is None:
        if sys.stdout.isatty():
            config = open_tui()
        else:
            config = DEFAULT_CONFIG
    elif isinstance(config, str):
        config = load_config(config)

    findall = True
    interactive = sys.stdout.isatty()
    verbose = True

    dio = DigItOut(config, findall, interactive, verbose, context)
    return dio.search(target)


def digitout_silent(target, config=None, context=None):
    """
    Silent version of [digitout_verbose][digitout.app.digitout_verbose]. It is dedicated to the users
    who don't want the results to get printed in the console. This is a good choice
    if one would like to integrate digitout with his application.

    Arguments and returned value are the same as for [digitout_verbose][digitout.app.digitout_verbose].
    """
    if config is None:
        config = DEFAULT_CONFIG
    elif isinstance(config, str):
        config = load_config(config)

    findall = False
    interactive = False
    verbose = False

    dio = DigItOut(config, findall, interactive, verbose, context)
    return dio.search(target)
