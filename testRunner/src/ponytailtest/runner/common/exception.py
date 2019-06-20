# -*- coding: utf-8 -*-


class TesterException(Exception):
    pass


class ScriptException(Exception):
    pass


class ElementFoundTimeoutException(ScriptException):
    pass


class ElementClickException(ScriptException):
    pass


class ElementSetValueException(ScriptException):
    pass


class ElementSelectException(ScriptException):
    pass
