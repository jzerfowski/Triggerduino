import serial
import ctypes
import logging
import numpy as np

class TriggerStruct(ctypes.Structure):
    """
    This has to represent the struct Trigger in the arduino's DAC.h (the order of the variables matters!)
    """
    _fields_ = [('channel', ctypes.c_int16),
                ('value', ctypes.c_int16),
                ('duration', ctypes.c_int16)
                ]

    def __str__(self):
        return f"Trigger on channel {self.channel}: value {self.value}, duration {self.duration}"


class Triggerduino:
    def __init__(self, serial_port, num_channels):
        self.serial_port = serial_port
        self.num_channels = num_channels

        logging.info(f"Triggerduino registered on serial port {self.serial_port.name}")

    def sendSignal(self, channel, value, duration):
        trigger = TriggerStruct(channel=channel, value=value, duration=duration)
        if value not in range(0, 4096): logging.warning("Value should be between 0 and 4095")
        self.sendTrigger(trigger)

    def sendTrigger(self, trigger):
        self.sendTriggers([trigger])

    def sendTriggers(self, triggers):
        triggers_b = bytearray()
        for trigger in triggers:
            triggers_b.extend(bytearray(trigger))

        self.serial_port.write(triggers_b)
        self.serial_port.flush()
        logging.debug(f"Serial data: {triggers_b}")

        for trigger in triggers:
            logging.info(f"Trigger sent: Channel {trigger.channel}, value: {trigger.value}, duration: {trigger.duration}ms");


def monitor_serial(stop, ser):
    while not stop():
        line = ser.readline()
        if line:
            print(line)
