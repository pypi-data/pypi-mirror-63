#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import six
from flask import current_app

try:
    from flask_wtf import FlaskForm
except ImportError:
    from flask_wtf import Form as FlaskForm

from wtforms.validators import ValidationError

__version__ = "0.3.0"


def required_if(
    depend_name=None,
    op=None,
    value=None,
    checks=[],
    error_msg="This field is required",
):
    def check_field(form, field):
        data = field.data
        if isinstance(data, six.string_types):
            data = data.strip()

        if data:
            return

        checks_ = checks or [(depend_name, op, value)]
        logics = 0
        for dep_name, op_, val in checks_:
            depend_data = getattr(form, dep_name).data
            if isinstance(depend_data, six.string_types):
                depend_data = depend_data.strip()

            if depend_data:
                func = getattr(operator, op_, None)
                logic1 = func and func(depend_data, val)
                logic2 = (not func) and getattr(depend_data, op_)(val)
                if logic1 or logic2:
                    logics += 1

        if logics == len(checks_):
            raise ValidationError(error_msg)

    return check_field


class ToppingForm(FlaskForm):
    __lowers__ = []
    __uppers__ = []
    __nostrips__ = []
    __excludes__ = []
    __aliases__ = {}

    def parse_form(self):
        lowers = self.get_attrs("lowers")
        uppers = self.get_attrs("uppers")
        nostrips = self.get_attrs("nostrips")
        excludes = self.get_attrs("excludes")
        aliases = self.get_attrs("aliases")
        field_name = current_app.config.get("WTF_CSRF_FIELD_NAME")
        if field_name:
            excludes.append(field_name)

        dct = {}
        for name, field in self._fields.items():
            if name in excludes:
                continue

            data = field.data
            if name in lowers:
                data = data.lower()
            elif name in uppers:
                data = data.upper()

            if name not in nostrips and isinstance(data, six.string_types):
                data = data.strip()

            dct[aliases.get(name, name)] = data

        return dct

    def get_attrs(self, kind="lowers"):
        attrs_ = []
        attr_name = "__{}__".format(kind)
        for kls in self.__class__.__mro__:
            if kls.__name__ == "ToppingForm":
                break

            attrs_.extend(kls.__dict__.get(attr_name, []))

        return list(set(attrs_))
