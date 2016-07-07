#!/usr/bin/env python3

import curses

class Speed_Monitor(object):

    def __init__(self):
        self.screen = curses.initscr()
        self.y, self.x = self.screen.getmaxyx()

    def refresh_monitor(self, status, **file_info):
        self.screen.clear()
        for i, t in enumerate(sorted(list(status.keys()))):
            self.screen.addstr(i, 0, '{}  {:10}'.format(t, status[t]))
        self.screen.addstr(self.y - 1, 0, '{}/{}bytes {:04.2f}%downloaded'.format(
                    file_info['downloaded'],
                    file_info['total'],
                    file_info['downloaded']/file_info['total']*100
                ))
        self.screen.refresh()

    def finish_monitor(self):
        curses.endwin()
