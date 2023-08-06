import sys
from functools import wraps
from .config import make_default_config
from .app import digitout_silent, digitout_verbose

class CallableModule(type(sys)):

    def __init__(self):
        super().__init__(__name__)
        self.make_default_config = make_default_config
        self.digitout_silent = digitout_silent
        self.digitout_verbose = digitout_verbose
        self._orig_module = sys.modules[__name__]

    @wraps(digitout_verbose)
    def __call__(self, *args, **kwargs):
        return digitout_verbose(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._orig_module, name)

sys.modules[__name__] = CallableModule()

