""" stopwatch.py

Contains the StopWatch class to be used with a Raspberry Pi and a 7-segment
LED display with a TM1637 control chip.

Read more at:
https://thingsdaq.org/2022/10/02/7-segment-led-display-with-raspberry-pi/

Author: Eduardo Nigro
    rev 0.0.1
    2022-10-02

"""
# Importing modules and classes
import time
import tm1637
import numpy as np
from pynput import keyboard


class StopWatch:
    """
    The class to represent a digital stopwatch.

    **StopWatch** runs on a Raspberry PI and uses a 4-digit 7-segment display
    with a TM1637 control chip.

    The following keyboard keys are used:

        * ``'s'`` to start/stop the timer.
        * ``'r'`` to reset the timer.
        * ``'q'`` to quit the application.
    
    """
    def __init__(self):
        """
        Class constructor.

        """
        # Creating 4-digit 7-segment display object
        self.tm = tm1637.TM1637(clk=18, dio=17)  # Using GPIO pins 18 and 17
        self.tm.show('00 0')  # Initializing stopwatch display
        # Creating keyboard event listener object
        self.myevent = keyboard.Events()
        self.myevent.start()
        # Defining time control variables (in seconds)
        self.treset = 60  # Time at which timer resets
        self.ts = 0.02  # Execution loop time step
        self.tdisp = 0.1  # Display update period
        self.tstart = 0  # Start time
        self.tstop = 0  # Stop time
        self.tcurr = 0  # Current time
        self.tprev = 0  # Previous time
        # Defining execution flow control flags
        self.run = False  # Timer run flag
        self.quit = False  # Application quit flag
        # Running execution loop
        self.runExecutionLoop()

    def runExecutionLoop(self):
        """
        Run the execution loop for the stopwatch.

        """
        # Running until quit request is received
        while not self.quit:
            # Pausing to make CPU life easier
            time.sleep(self.ts)
            # Updating current time value
            self.update_time()
            # Handling keyboard events
            self.handle_event()
            # Checking if automatic reset time was reached
            if self.tcurr >= self.treset:
                self.stop_watch()
                self.reset_watch()
                self.start_watch()
            # Updating digital display
            self.update_display()
            # Stroing previous time step
            self.tprev = self.tcurr

    def handle_event(self):
        """
        Handle non-blocking keyboard inputs that control stopwatch.

        """
        # Getting keyboard event
        event = self.myevent.get(0.0)
        if event is not None:
            # Checking for timer start/stop 
            if event.key == keyboard.KeyCode.from_char('s'):
                if type(event) == keyboard.Events.Release:
                    if not self.run:
                        self.run = True
                        self.start_watch()
                    elif self.run:
                        self.run = False
                        self.stop_watch()
            # Checking for timer reset
            elif event.key == keyboard.KeyCode.from_char('r'):
                if type(event) == keyboard.Events.Release:
                    if not self.run:
                        self.reset_watch()
                    elif self.run:
                        print('Stop watch before resetting.')
            # Checking for application quit
            elif event.key == keyboard.KeyCode.from_char('q'):
                self.quit = True
                self.tm.write([0, 0, 0, 0])
                print('Good bye.')

    def start_watch(self):
        """ Update start time. """
        self.tstart = time.perf_counter()

    def stop_watch(self):
        """ Update stop time. """
        self.tstop = self.tcurr

    def reset_watch(self):
        """ Reset timer. """
        self.tstop = 0
        self.tm.show('00 0')

    def update_time(self):
        """ Update timer value. """
        if self.run:
            self.tcurr = time.perf_counter() - self.tstart + self.tstop

    def update_display(self):
        """ Update digital display every 'tdisp' seconds. """
        if (np.floor(self.tcurr/self.tdisp) - np.floor(self.tprev/self.tdisp)) == 1:
            # Creating timer display string parts (seconds, tenths of a second)
            if int(self.tcurr) < 10:
                tsec = '0' + str(int(self.tcurr))
            else:
                tsec = str(int(self.tcurr))
            ttenth = str(int(np.round(10*(self.tcurr-int(self.tcurr)))))
            # Showing string on digital display
            self.tm.show(tsec + ' ' + ttenth)

            
# Running instance of StopWatch class
if __name__ == "__main__":
    StopWatch()