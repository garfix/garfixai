from platform import system
from os.path import abspath, exists
from urllib.request import pathname2url

system = system()


class PlaysoundException(Exception):
    pass



def _playsoundNix(sound, block = True):
    """Play a sound using GStreamer.

    Inspired by this:
    https://gstreamer.freedesktop.org/documentation/tutorials/playback/playbin-usage.html
    """

    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    if sound.startswith(('http://', 'https://')):
        playbin.props.uri = sound
    else:
        path = abspath(sound)
        if not exists(path):
            raise PlaysoundException(u'File not found: {}'.format(path))
        playbin.props.uri = 'file://' + pathname2url(path)

    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise PlaysoundException(
            "playbin.set_state returned " + repr(set_result))

    # FIXME: use some other bus method than poll() with block=False
    # https://lazka.github.io/pgi-docs/#Gst-1.0/classes/Bus.html
    if block:
        bus = playbin.get_bus()
        try:
            bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
        finally:
            playbin.set_state(Gst.State.NULL)


def playsound(sound, block = True):
    '''
    Mostly written so that when this is run on python3 on macOS, it can invoke
    python2 on macOS... but maybe this idea could be useful on linux, too.
    '''
    from inspect    import getsourcefile
    from os.path    import abspath, exists
    from subprocess import check_call
    from threading  import Thread

    PythonBin = '/usr/bin/python3'

    class PropogatingThread(Thread):
        def run(self):
            self.exc = None
            try:
                self.ret = self._target(*self._args, **self._kwargs)
            except BaseException as e:
                self.exc = e

        def join(self, timeout = None):
            super().join(timeout)
            if self.exc:
                raise self.exc
            return self.ret

    # Check if the file exists...
    if not exists(abspath(sound)):
        raise PlaysoundException('Cannot find a sound with filename: ' + sound)

    playsoundPath = abspath(getsourcefile(lambda: 0))

    t = PropogatingThread(target = lambda: check_call([PythonBin, playsoundPath, sound]))
    t.start()
    if block:
        t.join()


if __name__ == '__main__':
    # block is always True if you choose to run this from the command line.
    from sys import argv
    _playsoundNix(argv[1])
