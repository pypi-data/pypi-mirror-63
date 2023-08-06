import toml
import xdg

_DEFAULT_CONFIG_TOML = """
[engine]
stringifier = 'repr(obj)[:100]'
max_check_count = inf
max_depth = 5

[match]
expression = 'lambda value: True'
target = 'value' # value/item/iter/attr

[traversal.item]
inspect_values = true
inspect_keys = false
iterator = 'subscribe_from_keys' # call_items_method/zip_keys_and_values/subscribe_from_keys

[traversal.iter]
inspect = true
max_count = 5

[traversal.attr]
inspect = true
skip_types = ['bool', 'int', 'float', 'complex', 'bytes', 'bytearray', 'str', 'dict', 'list', 'set', 'frozenset', 'memoryview', 'type(None)']
skip_functions = false
skip_methods = false
skip_private = false
skip_dunders = false

[traversal.call]
inspect = true
skip_callables = []
skip_classes = true
skip_genfunc = false
"""

def make_default_config():
    return toml.loads(_DEFAULT_CONFIG_TOML)

DEFAULT_CONFIG = make_default_config()
DEFAULT_CONFIG_NAME = '<default>'

APP_NAME = 'digitout'
CONFIG_DIR = xdg.XDG_CONFIG_HOME / APP_NAME
CONFIGS_DIR = CONFIG_DIR / 'configs'
SESSION_PATH = CONFIG_DIR / 'session.toml'

def load_session():
    allowed_configs = list_configs()
    try:
        with SESSION_PATH.open() as fh:
            session = toml.load(fh)
            if session['config'] not in allowed_configs:
                session['config'] = DEFAULT_CONFIG_NAME
    except Exception:
        session = dict(config=DEFAULT_CONFIG_NAME)
    return session, allowed_configs

def save_session(session):
    with SESSION_PATH.open('w+') as fh:
        toml.dump(session, fh)

def init_config_dir():
    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)

def config_path(config_name):
    return CONFIGS_DIR.joinpath(config_name).with_suffix('.toml')

def list_configs():
    return [DEFAULT_CONFIG_NAME] + list(sorted([p.with_suffix('').name for p in CONFIGS_DIR.glob('*.toml')]))

def load_config(config_name):
    if config_name == DEFAULT_CONFIG_NAME:
        config = DEFAULT_CONFIG
    else:
        with config_path(config_name).open() as fh:
            config = toml.load(fh)
    return config

def save_config(config_name, config):
    if config_name != DEFAULT_CONFIG_NAME:
        with config_path(config_name).open('w+') as fh:
            toml.dump(config, fh)

def delete_config(config_name):
    config_path(config_name).unlink()

def get_from_config(config, path):
    value = config
    value_def = DEFAULT_CONFIG
    for key in path.split('.'):
        value_def = value_def.get(key)
        value = value.get(key, value_def)
    return value
