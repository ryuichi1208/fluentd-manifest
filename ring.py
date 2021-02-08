import numpy
import timeit
import collections


class CircularBuffer(object):
    buffer_methods = ('list', 'deque', 'roll')

    def __init__(self, buffer_size, buffer_method):
        self.content = None
        self.size = buffer_size
        self.method = buffer_method

    def update(self, scalar):
        if self.method == self.buffer_methods[0]:
            # Use list
            try:
                self.content.append(scalar)
                self.content.pop(0)
            except AttributeError:
                self.content = [0.] * self.size
        elif self.method == self.buffer_methods[1]:
            # Use collections.deque
            try:
                self.content.append(scalar)
            except AttributeError:
                self.content = collections.deque([0.] * self.size,
                                                 maxlen=self.size)
        elif self.method == self.buffer_methods[2]:
            # Use Numpy.roll
            try:
                self.content = numpy.roll(self.content, -1)
                self.content[-1] = scalar
            except IndexError:
                self.content = numpy.zeros(self.size, dtype=float)

# Testing and Timing
circular_buffer_size = 100
circular_buffers = [CircularBuffer(buffer_size=circular_buffer_size,
                                   buffer_method=method)
                    for method in CircularBuffer.buffer_methods]
timeit_iterations = 1e4
timeit_setup = 'from __main__ import circular_buffers'
timeit_results = []
for i, cb in enumerate(circular_buffers):
    # We add a convenient number of convenient values (see equality test below)
    code = '[circular_buffers[{}].update(float(j)) for j in range({})]'.format(
        i, circular_buffer_size)
    # Testing
    eval(code)
    buffer_content = [item for item in cb.content]
    assert buffer_content == range(circular_buffer_size)
    # Timing
    timeit_results.append(
        timeit.timeit(code, setup=timeit_setup, number=int(timeit_iterations)))
    print '{}: total {:.2f}s ({:.2f}ms per iteration)'.format(
        cb.method, timeit_results[-1],
        timeit_results[-1] / timeit_iterations * 1e3)
