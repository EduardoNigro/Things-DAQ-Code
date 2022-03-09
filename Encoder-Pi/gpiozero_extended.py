""" 
gpiozero_extended.py contains classes that are not implemented in GPIO Zero
(https://gpiozero.readthedocs.io/en/stable/) or that could use a different
implementation which is more suitable for automation projects.

Author: Eduardo Nigro
    rev 0.0.2
    2021-03-09
"""
import time
from gpiozero import DigitalOutputDevice, PWMOutputDevice, RotaryEncoder


class Motor:
    """
    The class to represent a DC motor controlled with an H-bridge driver.
    An encoder can be used to measure the angular position of the output shaft.

    Two types of drivers are allowed:

        * Single enable with dual PWM for forward and backward rotation control
        * Single PWM with dual enable for forward and backward rotation control

    Set up a motor with single enable:
    (SN754410 quadruple half-H driver chip)

        >>> from gpiozero_extended import Motor
        >>> mymotor = Motor(enable1=16, pwm1=17, pwm2=18)

    Set up a motor with single pwm:
    (L298 dual H-bridge motor speed controller board)

        >>> from gpiozero_extended import Motor
        >>> mymotor = Motor(enable1=16, enable2=17, pwm1=18)

    Set up a motor with single enable and an encoder with 450 PPR:
    (SN754410 quadruple half-H driver chip)

        >>> from gpiozero_extended import Motor
        >>> mymotor = Motor(
            enable1=16, pwm1=17, pwm2=18,
            encoder1=24, encoder2=25, encoderppr=450)

    :param enable1: The GPIO pin that is connected to the enable 1 of the driver.
    :type enable1: int or str
    :param enable2: The GPIO pin that is connected to the enable 2 of the driver.
        This value is ignored for a single enable driver.
    :type enable2: int or str
    :param pwn1: The GPIO pin that is connected to the PWM 1 of the driver.
    :type pwm1: int or str
    :param pwm2: The GPIO pin that is connected to the PWM 2 of the driver.
        This value is ignored for a single PWM driver.
    :type pwm2: int or str
    :param encoder1: The GPIO pin that is connected to the encoder phase A.
    :type encoder1: int or str
    :param encoder2: The GPIO pin that is connected to the encoder phase B.
    :type encoder2: int or str
    :param encoderppr: The number of Pulses Per Revolution (PPR) of the encoder.
        Default value is ``300``.
    :type encoderppr: int

    .. note::
        Always use `del` to delete the motor object after it's used to
        release the GPIO pins.

    """

    def __init__(
        self, enable1=None, enable2=None, pwm1=None, pwm2=None,
        encoder1=None, encoder2=None, encoderppr=300):
        """
        Class constructor.

        """
        # Identifying motor driver type and assigning appropriate GPIO pins
        if pwm1 and pwm2:
            # Driver with 1 enable and 2 PWM inputs
            # Example: SN754410 quadruple half-H driver chip
            if not enable1:
                raise Exception('"enable1" pin is undefined.')
            self._dualpwm = True
            self._enable1 = DigitalOutputDevice(enable1)
            self._pwm1 = PWMOutputDevice(pwm1)
            self._pwm2 = PWMOutputDevice(pwm2)
        elif enable1 and enable2:
            # Driver with 2 enables and 1 PWM input
            # Example: L298 dual H-bridge motor speed controller board
            if not pwm1:
                raise Exception('"pwm1" pin is undefined.')
            self._dualpwm = False
            self._enable1 = DigitalOutputDevice(enable1)
            self._enable2 = DigitalOutputDevice(enable2)
            self._pwm1 = PWMOutputDevice(pwm1)
        else:
            raise Exception('Pin configuration is incorrect.')
        # Checking for encoder
        if encoder1 and encoder2:
            self._encoder = RotaryEncoder(encoder1, encoder2, max_steps=0)
            self._ppr = encoderppr
        else:
            self._encoder = None
        # Initializing attributes
        self._value = 0  # Motor output value
        self._angle0 = 0  # Initial angular position


    def __del__(self):
        """
        Class destructor.
        
        """
        # Releasing GPIO pins
        if self._dualpwm:
            self._enable1.close()
            self._pwm1.close()
            self._pwm2.close()
        else:
            self._enable1.close()
            self._enable2.close()
            self._pwm1.close()
        if self._encoder:
            time.sleep(1)  # Added this to avoid segmentation fault :(
            self._encoder.close()

    @property
    def value(self):
        """
        Contains the motor output level (`read only`).
        Values can be between ``-1`` (full speed backward) and ``1`` (full
        speed forward), with ``0`` being stopped.

        """
        return self._value

    @value.setter
    def value(self, _):
        print('"value" is a read only attribute.')

    def get_angle(self):
        """
        Get the value of the encoder output angle.

        >>> mymotor.get_angle()

        """
        if self._encoder:
            angle = 360 / self._ppr * self._encoder.steps - self._angle0
        else:
            angle = None
        return angle

    def reset_angle(self):
        """
        Reset the encoder output angle.

        >>> mymotor.reset_angle()

        """
        if self._encoder:
            self._angle0 = 360 / self._ppr * self._encoder.steps


    def set_output(self, output, brake=False):
        """
        Set motor output.

        :param output: The PWM duty cycle value between ``-1`` and ``1``.
            A value of ``0`` stops the motor.
        :type output: float

        :param brake: The motor brake option used when duty cycle is zero.
            Brake is applied when ``True``. Motor is floating when ``False``.
        :type brake: bool

        Set output to ``0.5``:

            >>> mymotor.set_output(0.5)

        Set output to ``0.25`` (reverse rotation):

            >>> mymotor.set_output(-0.25)

        Stop motor and apply brake:

            >>> mymotor.set_output(0, brake=True)

        """
        # Limiting output
        if output > 1:
            output = 1
        elif output < -1:
            output = -1
        # Forward rotation
        if output > 0:
            if self._dualpwm:
                self._enable1.on()
                self._pwm1.value = output
                self._pwm2.value = 0
            else:
                self._enable1.on()
                self._enable2.off()
                self._pwm1.value = output
        # Backward rotation
        elif output < 0:
            if self._dualpwm:
                self._enable1.on()
                self._pwm1.value = 0
                self._pwm2.value = -output
            else:
                self._enable1.off()
                self._enable2.on()
                self._pwm1.value = -output
        # Stop motor
        elif output == 0:
            if brake:
                if self._dualpwm:
                    self._enable1.off()
                    self._pwm1.value = 0
                    self._pwm2.value = 0
                else:
                    self._enable1.off()
                    self._enable2.off()
                    self._pwm1.value = 0
            else:
                if self._dualpwm:
                    self._enable1.on()
                    self._pwm1.value = 0
                    self._pwm2.value = 0
                else:
                    self._enable1.on()
                    self._enable2.on()
                    self._pwm1.value = 0
        # Updating output value property
        self._value = output