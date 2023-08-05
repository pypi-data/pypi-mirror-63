#!/usr/bin/env python3
'''
Real-time plot demo using overlain sine waves.

Copyright (C) 2016 Simon D. Levy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import numpy
from realtime_plot import RealtimePlotter


# Simple example with threading

class _SinePlotter(RealtimePlotter):

  def __init__(self):
    RealtimePlotter.__init__(self, [(-1, +1)],
                             window_name='Sine and Cosine',
                             yticks=[(-1, 0, +1)],
                             styles=[('r--', 'b-')],
                             legends=[('sin', 'cos')])

    self.xcurr = 0

  def getValues(self):
    return self._getWave(numpy.sin), self._getWave(numpy.cos)

  def _getWave(self, fun):
    size = len(self.x)

    return fun(2 * numpy.pi * (float(self.xcurr) % size) / size)


def _update(plotter):
  from time import sleep

  while True:

    plotter.xcurr += 1
    sleep(.002)


if __name__ == '__main__':

  import threading

  plotter = _SinePlotter()

  thread = threading.Thread(target=_update, args=(plotter,))
  thread.daemon = True
  thread.start()

  plotter.start()
