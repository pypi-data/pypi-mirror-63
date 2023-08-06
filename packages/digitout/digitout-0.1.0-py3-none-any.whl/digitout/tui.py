import npyscreen as npys
import curses
import re
import enum
import sys
from copy import deepcopy
from math import inf
from types import SimpleNamespace
from .widgets import MainForm, Separator, Label, TitleComboEx, ConstrainedText, TitleConstrainedText, OptionMultiFreeListNarrow
from .config import DEFAULT_CONFIG, DEFAULT_CONFIG_NAME, save_config, load_config, delete_config, get_from_config, load_session, save_session, init_config_dir, list_configs

def _peep(target):
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    from peepshow import peep
    peep(target)

TargetKind = enum.IntEnum('TargetKind', ['value', 'item', 'iter', 'attr'], start=0)
DictIterator = enum.IntEnum('DictIterator', ['call_items_method', 'zip_keys_and_values', 'subscribe_from_keys'], start=0)

def get_lambda_parser(signature):
    def lambda_parser(body):
        return eval(signature + body, {}, {})
    return lambda_parser

def get_lambda_signature(index):
    args = ['value', 'key, value', 'index, value', 'name, value']
    return 'lambda ' + args[index] + ': '

def parse_count(value):
    if value == 'inf':
        return inf

    val = int(value)

    if val > 0:
        return val

    raise ValueError

def config_name_validator(value):
    regex = re.compile('^[a-zA-Z0-9_]+$')
    regex.match(value)[0]

def get_config_attr_callback(subconfig):
    def config_attr():
        form = npys.ActionPopup(name = 'Attributes')
        cb_skip_func = form.add(npys.Checkbox, name = "Skip functions")
        cb_skip_meth = form.add(npys.Checkbox, name = "Skip methods")
        cb_skip_priv = form.add(npys.Checkbox, name = "Skip non-public (_xyz, __xyz)")
        cb_skip_dund = form.add(npys.Checkbox, name = "Skip dunders (__xyz__)")

        form.add(Separator)
        opt_list = npys.OptionList()
        opt_list.options.append(OptionMultiFreeListNarrow("Don't visit instances of"))
        opt_dont_visit = form.add(npys.OptionListDisplay, values = opt_list.options, scroll_exit=True, max_height=None)
        opt_list.options[0].set(['bool', 'int', 'float', 'complex', 'bytes', 'bytearray', 'str', 'dict', 'list', 'set', 'frozenset', 'memoryview', 'type(None)'])

        widgets = SimpleNamespace()
        widgets.cb_skip_func = cb_skip_func
        widgets.cb_skip_meth = cb_skip_meth
        widgets.cb_skip_priv = cb_skip_priv
        widgets.cb_skip_dund = cb_skip_dund
        widgets.opt_dont_visit = opt_dont_visit

        load_subconfig_attr(subconfig, widgets)
        form.on_ok = lambda: store_subconfig_attr(subconfig, widgets)
        form.display()
        form.edit()
    return config_attr

def get_config_item_callback(subconfig):
    def config_item():
        form = npys.ActionPopup(name = 'Items of mappings')
        co_iterator = form.add(TitleComboEx, name="Iterator", values = ['obj.items()', 'zip(obj.keys(), obj.values())', '(key, obj[key] for key in obj.keys())'])
        #['Call items method', 'Zip keys and values', 'Subscribe from keys'])
        co_iterator.entry_widget.on_popup_close_callback = lambda widget: None
        co_iterator.value = 0

        widgets = SimpleNamespace()
        widgets.co_iterator = co_iterator

        load_subconfig_item(subconfig, widgets)
        form.on_ok = lambda: store_subconfig_item(subconfig, widgets)
        form.display()
        form.edit()

    return config_item

def get_config_iter_callback(subconfig):
    def config_iter():
        form = npys.ActionPopup(name = 'Items of iterables')
        ct_max_count = form.add(TitleConstrainedText, name='Max count', value = '5')
        ct_max_count.entry_widget.set_validator(parse_count)

        widgets = SimpleNamespace()
        widgets.ct_max_count = ct_max_count

        load_subconfig_iter(subconfig, widgets)
        form.on_ok = lambda: store_subconfig_iter(subconfig, widgets)
        form.display()
        form.edit()
    return config_iter

def get_config_call_callback(subconfig):
    def config_call():
        form = npys.ActionPopup(name = 'Values returned by callables')
        cb_skip_classes = form.add(npys.Checkbox, name = "Skip classes (__init__)")
        cb_skip_genfunc = form.add(npys.Checkbox, name = "Skip generator functions")

        form.add(Separator)
        opt_list = npys.OptionList()
        opt_list.options.append(OptionMultiFreeListNarrow('Skip callables named'))
        opt_skip_callables = form.add(npys.OptionListDisplay, values = opt_list.options, scroll_exit=True, max_height=None)
        opt_list.options[0].set(['exit'])

        widgets = SimpleNamespace()
        widgets.cb_skip_classes = cb_skip_classes
        widgets.cb_skip_genfunc = cb_skip_genfunc
        widgets.cb_skip_genfunc = cb_skip_genfunc
        widgets.opt_skip_callables = opt_skip_callables

        load_subconfig_call(subconfig, widgets)
        form.on_ok = lambda: store_subconfig_call(subconfig, widgets)
        form.display()
        form.edit()
    return config_call

def save_config_dialog(widgets, subconfigs):
    config_name = widgets.co_config.values[widgets.co_config.value]
    if config_name == DEFAULT_CONFIG_NAME:
        config_name = "Untitled"
    form = npys.ActionPopup(name = 'Save Config')

    ct_config_name = form.add(TitleConstrainedText, name = 'Config', value = config_name)

    form.add(Separator)

    ct_overwrite = form.add(ConstrainedText)
    ct_overwrite.editable = False

    def check_existing(value):
        ct_overwrite.value = ''
        try:
            config_name_validator(value)
        except Exception:
            raise
        else:
            if ct_config_name.value != DEFAULT_CONFIG_NAME and ct_config_name.value in widgets.co_config.values:
                if widgets.co_config.values.index(ct_config_name.value) == widgets.co_config.value:
                    ct_overwrite.value = '(current config)'
                else:
                    ct_overwrite.value = '(existing config)'
        finally:
            ct_overwrite.update()

    def update_co_config():
        if ct_config_name.value not in widgets.co_config.values:
            widgets.co_config.values.append(ct_config_name.value)
        widgets.co_config.value = widgets.co_config.values.index(ct_config_name.value)
        widgets.co_config.update()

    ct_config_name.entry_widget.set_validator(check_existing)
    form.on_ok = update_co_config
    check_existing(ct_config_name.value)
    form.display()
    form.edit()



def collect_config(widgets, subconfigs):
    coerce_count = lambda s: float(s) if s == 'inf' else int(s)

    traversal = deepcopy(subconfigs)
    traversal['item']['inspect_keys'] = widgets.cb_item_key.value
    traversal['item']['inspect_values'] = widgets.cb_item_val.value
    traversal['iter']['inspect'] = widgets.cb_iter.value
    traversal['attr']['inspect'] = widgets.cb_attr.value
    traversal['call']['inspect'] = widgets.cb_call.value

    config = {
        'engine': {
            'stringifier': widgets.stringifier.value,
            'max_check_count': coerce_count(widgets.max_check_count.value),
            'max_depth': coerce_count(widgets.max_depth.value),
            },

        'match': {
            'target': TargetKind(widgets.target.value).name,
            'expression': widgets.constraint_signature.value + widgets.constraint.value,
            },

        'traversal': traversal,
        }

    return config


def save_config_from_ui(config, widgets, subconfigs):
    config_name = widgets.co_config.values[widgets.co_config.value]
    save_config(config_name, config)
    save_config_in_session(widgets)

def load_config_to_ui(widgets, subconfigs, config_name=DEFAULT_CONFIG_NAME):

    config = load_config(config_name)

    # Target
    widgets.target.value = TargetKind[get_from_config(config, 'match.target')]
    sep = ': '
    signature, body = get_from_config(config, 'match.expression').split(': ', maxsplit=1)
    signature += sep

    widgets.constraint_signature.value = signature
    widgets.constraint.value = body

    # Settings
    widgets.stringifier.value = get_from_config(config, 'engine.stringifier')
    widgets.max_check_count.value = str(get_from_config(config, 'engine.max_check_count'))
    widgets.max_depth.value = str(get_from_config(config, 'engine.max_depth'))

    # Traversals
    widgets.cb_item_key.value = get_from_config(config, 'traversal.item.inspect_keys')
    widgets.cb_item_val.value = get_from_config(config, 'traversal.item.inspect_values')
    widgets.cb_iter.value = get_from_config(config, 'traversal.iter.inspect')
    widgets.cb_attr.value = get_from_config(config, 'traversal.attr.inspect')
    widgets.cb_call.value = get_from_config(config, 'traversal.call.inspect')

    # Subconfigs
    for key in subconfigs.keys():
        subconfigs[key].clear()
        subconfigs[key].update(get_from_config(config, 'traversal.' + key))

    for _, widget in vars(widgets).items():
        widget.update()

    save_config_in_session(widgets)

def save_config_in_session(widgets):
    session, _ = load_session()
    session['config'] = widgets.co_config.values[widgets.co_config.value]
    save_session(session)

def delete_config_from_ui(widgets, subconfigs):
    config_name = widgets.co_config.values[widgets.co_config.value]

    if config_name == DEFAULT_CONFIG_NAME:
        npys.notify_confirm("Default config cannot be deleted.", title='Delete Config')
    else:
        if npys.notify_yes_no(f"Is config {config_name!r} to be deleted?", title='Delete Config'):
            delete_config(config_name)
            widgets.co_config.values = list_configs()
            widgets.co_config.value = 0
            load_config_to_ui(widgets, subconfigs)


def load_subconfig_item(subconfig, widgets):
    widgets.co_iterator.value = DictIterator[get_from_config(subconfig, 'iterator')].value

def store_subconfig_item(subconfig, widgets):
    subconfig['iterator'] = DictIterator(widgets.co_iterator.value).name

def load_subconfig_iter(subconfig, widgets):
    widgets.ct_max_count.entry_widget.value = str(get_from_config(subconfig, 'max_count'))

def store_subconfig_iter(subconfig, widgets):
    subconfig['max_count'] = parse_count(widgets.ct_max_count.entry_widget.value)

def load_subconfig_attr(subconfig, widgets):
    widgets.cb_skip_func.value = subconfig['skip_functions']
    widgets.cb_skip_meth.value = subconfig['skip_methods']
    widgets.cb_skip_priv.value = subconfig['skip_private']
    widgets.cb_skip_dund.value = subconfig['skip_dunders']
    widgets.opt_dont_visit.values[0].value = subconfig['skip_types']

def store_subconfig_attr(subconfig, widgets):
    subconfig['skip_functions'] = widgets.cb_skip_func.value
    subconfig['skip_methods'] = widgets.cb_skip_meth.value
    subconfig['skip_private'] = widgets.cb_skip_priv.value
    subconfig['skip_dunders'] = widgets.cb_skip_dund.value
    subconfig['skip_types'] = widgets.opt_dont_visit.values[0].value

def load_subconfig_call(subconfig, widgets):
    widgets.cb_skip_classes.value = subconfig['skip_classes']
    widgets.cb_skip_genfunc.value = subconfig['skip_genfunc']
    widgets.opt_skip_callables.values[0].value = subconfig['skip_callables']

def store_subconfig_call(subconfig, widgets):
    subconfig['skip_classes'] = widgets.cb_skip_classes.value
    subconfig['skip_genfunc'] = widgets.cb_skip_genfunc.value
    subconfig['skip_callables'] = widgets.opt_skip_callables.values[0].value

def add_config(main, widgets, layout, subconfigs, allowed_configs):
    co_config = main.add(TitleComboEx, name="Config:", value = 0, values = allowed_configs , width = 45)
    def update_co_config_values(widget):
        widget.values = list_configs()
    co_config.entry_widget.on_popup_open_callback = lambda widget: update_co_config_values(widget)
    co_config.entry_widget.on_popup_close_callback = lambda widget: load_config_to_ui(widgets, subconfigs, config_name=widget.values[widget.value])

    bn_save = main.add(npys.ButtonPress, name = "New", relx = main.nextrelx + co_config.width, rely = co_config.rely)
    bn_save.whenPressed = lambda: save_config_dialog(widgets, subconfigs)

    bn_delete = main.add(npys.ButtonPress, name = "Delete", relx = main.nextrelx + co_config.width + 6, rely = co_config.rely)
    bn_delete.whenPressed = lambda: delete_config_from_ui(widgets, subconfigs)

    widgets.co_config = co_config.entry_widget

def add_target(main, widgets, layout, subconfigs):
    main.add(Label, name = "Target:")
    main.add(Separator)
    main.nextrelx += layout.indent

    co_target = main.add(TitleComboEx, name="Kind", value = 0, values = ['Value', 'Item of mapping', 'Item of iterable', 'Attribute'])

    ct_signature = main.add(TitleConstrainedText, name="Constraint", value = 'lambda value: ')
    ct_signature.editable = False

    ct_constr = main.add(ConstrainedText, value = 'True', rely = ct_signature.rely)
    ct_constr.set_validator(get_lambda_parser(ct_signature.value))

    orig_ct_signature_update = ct_signature.update
    orig_ct_signature_width = ct_constr.width
    orig_ct_signature_relx = ct_constr.relx
    def new_ct_signature_update(*args, **kwargs):
        ct_constr.relx = ct_signature.relx + ct_signature.text_field_begin_at + len(ct_signature.value)
        ct_constr.width = orig_ct_signature_width + orig_ct_signature_relx - ct_constr.relx - 1
        ct_constr.resize()
        return orig_ct_signature_update(*args, **kwargs)

    ct_signature.update = new_ct_signature_update
    ct_signature.update()

    def on_popup_close(widget):
        ct_signature.value = get_lambda_signature(widget.value)
        ct_constr.relx = ct_signature.relx + ct_signature.text_field_begin_at + len(ct_signature.value)
        ct_signature.display()
        ct_constr.display()

    co_target.entry_widget.on_popup_close_callback = on_popup_close
    main.nextrelx -= layout.indent

    widgets.target = co_target.entry_widget
    widgets.constraint_signature = ct_signature
    widgets.constraint = ct_constr

def add_settings(main, widgets, layout, subconfigs):
    main.add(Label, name = "Settings:")
    main.add(Separator)
    main.nextrelx += layout.indent

    ct_signature = main.add(TitleConstrainedText, name="Stringifier", value = 'lambda obj: ')
    ct_signature.editable = False

    ct_stringifier = main.add(ConstrainedText, value = 'repr(obj)[:100]', relx = ct_signature.relx + ct_signature.text_field_begin_at + len(ct_signature.value), rely = ct_signature.rely)
    ct_stringifier.set_validator(get_lambda_parser(ct_signature.value))

    ct_max_check_count = main.add(TitleConstrainedText, name='Checks limit', value = 'inf')
    ct_max_check_count.entry_widget.set_validator(parse_count)

    ct_max_depth = main.add(TitleConstrainedText, name='Depth limit', value = '15')
    ct_max_depth.entry_widget.set_validator(parse_count)

    main.nextrelx -= layout.indent

    widgets.stringifier = ct_stringifier
    widgets.max_check_count = ct_max_check_count.entry_widget
    widgets.max_depth = ct_max_depth.entry_widget

def add_visitors(main, widgets, layout, subconfigs):
    main.add(Label, name = "Visitors:")
    main.add(Separator)
    main.nextrelx += layout.indent

    cb_item_val = main.add(npys.Checkbox, name = "Values of mappings", width = 24)

    cb_item_key = main.add(npys.Checkbox, name = "Keys of mappings", width = 22, relx = cb_item_val.relx + cb_item_val.width,  rely = cb_item_val.rely)
    bn_item_key = main.add(npys.ButtonPress, name = "Configure", relx = main.nextrelx + layout.col0_width, rely = cb_item_key.rely)
    bn_item_key.whenPressed = get_config_item_callback(subconfigs['item'])

    cb_iter = main.add(npys.Checkbox, name = "Values of iterables", width = layout.col0_width)
    bn_iter = main.add(npys.ButtonPress, name = "Configure", relx = main.nextrelx + layout.col0_width, rely = cb_iter.rely)
    bn_iter.whenPressed = get_config_iter_callback(subconfigs['iter'])

    cb_attr = main.add(npys.Checkbox, name = "Attributes", width = layout.col0_width)
    bn_attr = main.add(npys.ButtonPress, name = "Configure", relx = main.nextrelx + layout.col0_width, rely = cb_attr.rely)
    bn_attr.whenPressed = get_config_attr_callback(subconfigs['attr'])

    cb_call = main.add(npys.Checkbox, name = "Values returned by callables", width = layout.col0_width)
    bn_call = main.add(npys.ButtonPress, name = "Configure", relx = main.nextrelx + layout.col0_width, rely = cb_call.rely)
    bn_call.whenPressed = get_config_call_callback(subconfigs['call'])

    widgets.cb_item_key = cb_item_key
    widgets.cb_item_val = cb_item_val
    widgets.cb_iter = cb_iter
    widgets.cb_attr = cb_attr
    widgets.cb_call = cb_call

    main.nextrelx -= layout.indent

def add_footnote(main, widgets, layout, subconfigs):

    main.add(Label, name = "Caution:")
    main.add(Separator)
    main.nextrelx += layout.indent

    ct_disclaimer1 = main.add(npys.Textfield, value = 'Side effects of accessing Python objects may cause')
    ct_disclaimer2 = main.add(npys.Textfield, value = 'damage to your system. Do this at your own risk!!!')
    ct_disclaimer1.color = ct_disclaimer2.color = 'CAUTION'
    ct_disclaimer1.editable = ct_disclaimer2.editable = False

    main.nextrelx -= layout.indent

def get_build_ui(config, config_name=None):
    def build_ui(window):
        main  = MainForm(name = "DigItOut",)
        widgets = SimpleNamespace()
        layout = SimpleNamespace(indent = 2, col0_width = 45)
        subconfigs = {key: {} for key in DEFAULT_CONFIG['traversal'].keys()}

        session, allowed_configs = load_session()

        add_config(main, widgets, layout, subconfigs, allowed_configs)
        main.add(Separator)
        add_target(main, widgets, layout, subconfigs)
        main.add(Separator)
        add_settings(main, widgets, layout, subconfigs)
        main.add(Separator)
        add_visitors(main, widgets, layout, subconfigs)
        main.add(Separator)
        add_footnote(main, widgets, layout, subconfigs)


        if config_name is None:
            config_name_ = session['config']
        else:
            config_name_ = config_name

        widgets.co_config.value = widgets.co_config.values.index(config_name_)

        load_config_to_ui(widgets, subconfigs, config_name_)
        main.edit()
        config_ = collect_config(widgets, subconfigs)
        save_config_from_ui(config_, widgets, subconfigs)
        return config.update(config_)

    return build_ui

def open_tui(config_name=None):
    try:
        init_config_dir()
        config = {}
        npys.wrapper_basic(get_build_ui(config, config_name))
        return config
    except KeyboardInterrupt:
        pass
