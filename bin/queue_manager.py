#!/usr/bin/python
# Queue manager
# This module depends on pyinotify: http://pyinotify.sourceforge.net/
# should listen for new files on a directory, decompress archives
# and pass archive.zip & tests.zip to commander, waits for the result,
# applies penalty & submits back the results.
#
# Note, last two steps should be grouped together: queue_manager should
# call a script ./callback located in archive which does this shit.


import sys
import tempfile
import shutil
import misc

from subprocess import check_call
from os.path import join
from pyinotify import WatchManager, Notifier, ProcessEvent, EventsCodes


__author__ = 'Alexandru Mosoi <brtzsnr@gmail.com>'


class _QueueManager(ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        _process_job(event.path, event.name)


def _process_job(path, name):
    location = tempfile.mkdtemp(prefix='vmchecker-')
    archive = join(path, name)
    print 'Expanding archive `%s\' at `%s\'.' % (archive, location)

    check_call(('tar', '-C', location, '-xzvf', archive))

    print 'Cleaning `%s\'' % location
    shutil.rmtree(location)


def main():
    wm = WatchManager()
    notifier = Notifier(wm, _QueueManager())
    wm.add_watch(vmcheckerpaths.dir_queue(), EventsCodes.ALL_FLAGS['IN_CLOSE_WRITE'])
    notifier.loop(callback=lambda self: self.proc_fun())


if __name__ == '__main__':
    main()