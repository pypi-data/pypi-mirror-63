import sys
from colorama import Fore, Style

class SearchResult(Exception):
    pass

class TargetFound(SearchResult):

    def __init__(self, path, match):
        self.path = path
        self.match = match
        super().__init__(f'Match found at: {path}')

class TargetNotFound(SearchResult):

    def __init__(self):
        super().__init__(f'No matches found')

class Matcher:
    _check_count = 0

    def __init__(self, func, reporter, target_found_callback):
        self._func = func
        self._reporter = reporter
        self._target_found_callback = target_found_callback

    def set_up(self, stringifier, max_check_count, **kwargs):
        self._stringifier = stringifier
        self._max_check_count = max_check_count

    def _make_log_entry(self, path, value, **kwargs):
        value_str = self._stringifier(value)
        #print(f'{Fore.MAGENTA}{self._check_count} {Fore.GREEN}{path}:{Style.RESET_ALL} {value_str}')
        self._reporter(f'{Fore.GREEN}{path}:{Style.RESET_ALL} {value_str}')

        self._check_count += 1
        if self._check_count >= self._max_check_count:
            raise TargetNotFound()

    def check(self, path, **kwargs):
        self._make_log_entry(path, **kwargs)

        try:
            target_found = self._func(**kwargs)
        except Exception as exc:
            self._reporter(f'Error while accessing {path}: {exc}', file=sys.stderr)
        else:
            if target_found:
                self._target_found_callback(path, kwargs)

class ValueMatcher(Matcher):
    pass

class AttrMatcher(Matcher):
    pass

class IterMatcher(Matcher):
    pass

class ItemMatcher(Matcher):
    pass

class CallMatcher(Matcher):
    pass
