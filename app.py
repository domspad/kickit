#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Script description here
"""


from __future__ import print_function, absolute_import, division
import asyncio
import urwid
from ui import PatternWidget
from loop import read_pattern_and_schedule, DRUM_PATTERN


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    return key


def set_drum(pattern_widget, block_widget, index=None):
    assert index is not None
    on = not block_widget.on
    pattern_name = pattern_widget.name
    DRUM_PATTERN[pattern_name][index] = on
    pattern_widget.pattern = DRUM_PATTERN[pattern_name]
    pattern_widget.redraw()


def run(args):
    pile = urwid.Pile([
        PatternWidget(name, DRUM_PATTERN[name], onclick=set_drum)
        for name in ['hhat', 'snare', 'kick']
    ])

    asyncio_loop = asyncio.get_event_loop()
    asyncio_loop.call_soon(read_pattern_and_schedule, asyncio_loop)
    evl = urwid.AsyncioEventLoop(loop=asyncio_loop)
    urwid_loop = urwid.MainLoop(urwid.Filler(pile), event_loop=evl, unhandled_input=exit_on_q)
    urwid_loop.run()


if '__main__' == __name__:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    args = parser.parse_args()
    run(args)
