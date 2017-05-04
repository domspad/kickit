# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
from functools import partial
import urwid


class BlockWidget(urwid.WidgetWrap):
    def __init__(self, on=False, onclick=None):
        self._on = bool(on)
        self.text = urwid.Text(u'', wrap='clip')
        self.redraw()
        self.onclick = onclick
        super(BlockWidget, self).__init__(self.text)

    def selectable(self):
        return bool(self.onclick)

    def __repr__(self):
        return '%s(on=%r, onclick=%r)' % (self.__class__.__name__,
                                          self.on, self.onclick)

    @property
    def on(self):
        return self._on

    @on.setter
    def on(self, val):
        self._on = bool(val)
        self.redraw()

    def redraw(self):
        if self.on:
            self.text.set_text([
                u'╭───╮\n',
                u'│███│\n',
                u'╰───╯\n',
            ])
        else:
            self.text.set_text([
                u'╭───╮\n',
                u'│   │\n',
                u'╰───╯\n',
            ])

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            if self.onclick:
                self.onclick(self)


class PatternWidget(urwid.WidgetWrap):
    def __init__(self, name, pattern, onclick=None):
        self.onclick = onclick
        self.name = name
        self._pattern = pattern
        title = urwid.Text('\n' + name.upper())
        self.columns = urwid.Columns([title])
        self.redraw()
        super(PatternWidget, self).__init__(self.columns)

    def callback(self, index):
        if self.onclick:
            return partial(self.onclick, self, index=index)

    def redraw(self):
        self.columns.contents[1:] = [
            (BlockWidget(on=val, onclick=self.callback(idx)),
             self.columns.options())
            for idx, val in enumerate(self.pattern)
        ]

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, pattern):
        self._pattern = pattern
        self.redraw()
