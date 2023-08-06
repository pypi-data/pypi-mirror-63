import weakref
import npyscreen as npys

class RestrictiveText(npys.wgtextbox.Textfield):

    def _print(self):

        if self.safe_to_exit():
            self.color = 'DEFAULT'
        else:
            self.color = 'CRITICAL'

        if self.do_colors():
            self.parent.curses_pad.addnstr(self.rely, self.relx, self.value, self.width, self.parent.theme_manager.findPair(self))
        else:
            self.parent.curses_pad.addnstr(self.rely, self.relx, self.value, self.width)

class ConstrainedText(RestrictiveText):

    _validator = lambda self, value: True

    def set_validator(self, validator):
        self._validator = validator

    def safe_to_exit(self):
        try:
            self._validator(self.value)
        except Exception:
            return False
        return True

class TitleConstrainedText(npys.TitleText):
    _entry_type = ConstrainedText


class Separator(npys.wgwidget.Widget):
    "This widget is invisible and does nothing.  Which is sometimes important."
    def __init__(self, screen, *args, **keywords):
        super().__init__(screen, *args, **keywords)
        self.height = 1
        self.widget = 0
        self.parent = screen
        self.editable = False
    def display(self):
        pass
    def update(self, clear=False):
        pass
    def set_editable(self, value):
        pass
    def get_editable(self):
        return self.editable
    def clear(self, usechar=' '):
        pass
    def calculate_area_needed(self):
        return 0,0

class Label(npys.TitleText):
    _entry_type = Separator

class ComboBoxEx(npys.ComboBox):

    on_popup_open_callback = lambda self, widget: None
    on_popup_close_callback = lambda self, widget: None

    def h_change_value(self, input):
        "Pop up a window in which to select the values for the field"
        self.on_popup_open_callback(self)
        F = npys.Popup(name = self.name)
        l = F.add(npys.wgmultiline.MultiLine,
            values = [self.display_value(x) for x in self.values],
            return_exit=True, select_exit=True,
            value=self.value)
        l.cursor_line = self.value
        F.display()
        l.edit()
        self.value = l.value
        self.on_popup_close_callback(self)

class TitleComboEx(npys.TitleText):
    _entry_type = ComboBoxEx

class MainForm(npys.Form):
    OK_BUTTON_TEXT = 'OK'

class OptionChangerNarrow(npys.fmPopup.ActionPopup):
    def on_ok(self,):
        self.OPTION_TO_CHANGE.set_from_widget_value(self.OPTION_WIDGET.value)

class OptionNarrow(npys.apOptions.Option):
    def change_option(self):
        option_changing_form = OptionChangerNarrow()
        option_changing_form.OPTION_TO_CHANGE = weakref.proxy(self)
        if self.documentation:
            explanation_widget = option_changing_form.add(wgmultiline.Pager,
                                                        editable=False, value=None,
                                                        max_height=(option_changing_form.lines - 3) // 2,
                                                        autowrap=True,
                                                        )
            option_changing_form.nextrely += 1
            explanation_widget.values = self.documentation


        option_widget = option_changing_form.add(self.WIDGET_TO_USE,
                                                    name=self.get_name_user(),
                                                    **self.option_widget_keywords
                                                )
        option_changing_form.OPTION_WIDGET = option_widget
        self._set_up_widget_values(option_changing_form, option_widget)
        option_changing_form.edit()

class OptionMultiFreeListNarrow(OptionNarrow):
    WIDGET_TO_USE = npys.wgeditmultiline.MultiLineEdit
    DEFAULT = []
    def _set_up_widget_values(self, option_form, main_option_widget):
        main_option_widget.value = "\n".join(self.get())

    def set_from_widget_value(self, vl):
        self.set(vl.split("\n"))
