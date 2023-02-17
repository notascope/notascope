# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashDiff(Component):
    """A DashDiff component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- newCode (string; required):
    new code.

- oldCode (string; required):
    old code."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, oldCode=Component.REQUIRED, newCode=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'newCode', 'oldCode']
        self._type = 'DashDiff'
        self._namespace = 'notascope_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'newCode', 'oldCode']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['oldCode', 'newCode']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashDiff, self).__init__(**args)
