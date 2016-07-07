#!/usr/bin/env python3

import curses

class Speed_Monitor(object):

    def __init__(self):
        self.screen = curses.initscr()

    def refresh_monitor(self, status):
        self.screen.clear()
        for i, t in enumerate(sorted(list(status.keys()))):
            self.screen.addstr(i, 0, '{}  {:10}'.format(t, status[t]))
        self.screen.refresh()

    def finish_monitor(self):
        curses.endwin()
