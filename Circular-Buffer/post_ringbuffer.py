""" post_ringbuffer.py 

THis example shows how to implement a circular buffer with a Python class.

For more details go to my post:
https://thingsdaq.org/2023/04/18/circular-buffer-in-python/

Author: Eduardo Nigro
    rev 0.0.1
    2023-04-18

"""
class RingBuffer:
    """ Class that implements a not-yet-full buffer. """
    def __init__(self, bufsize):
        self.bufsize = bufsize
        self.data = []

    class __Full:
        """ Class that implements a full buffer. """
        def add(self, x):
            """ Add an element overwriting the oldest one. """
            self.data[self.currpos] = x
            self.currpos = (self.currpos+1) % self.bufsize
        def get(self):
            """ Return list of elements in correct order. """
            return self.data[self.currpos:]+self.data[:self.currpos]

    def add(self,x):
        """ Add an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.bufsize:
            # Initializing current position attribute
            self.currpos = 0
            # Permanently change self's class from not-yet-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data


# Sample usage to recreate example figure values
import numpy as np
if __name__ == '__main__':

    # Creating ring buffer
    x = RingBuffer(10)
    # Adding first 4 elements
    x.add(5); x.add(10); x.add(4); x.add(7)
    # Displaying class info and buffer data
    print(x.__class__, x.get())  

    # Creating fictitious sampling data list
    data = [1, 11, 6, 8, 9, 3, 12, 2]

    # Adding elements until buffer is full
    for value in data[:6]:
        x.add(value)
    # Displaying class info and buffer data
    print(x.__class__, x.get())

    # Adding data simulating a data acquisition scenario
    print('')
    print('Mean value = {:0.1f}   |  '.format(np.mean(x.get())), x.get())
    for value in data[6:]:
        x.add(value)
        print('Mean value = {:0.1f}   |  '.format(np.mean(x.get())), x.get())
