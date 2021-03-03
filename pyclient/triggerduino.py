import serial
import ctypes
import logging

logger = logging.getLogger(__name__)


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
    def __init__(self, serial_port=None, lsl_outlet=None):
        self.serial_port = serial_port

        # if an LSL-Outlet should be used it needs exactly 4 channels
        self.lsl_outlet = lsl_outlet
        if self.serial_port:
            logger.info(f"Triggerduino registered on serial port {self.serial_port.name}")
        else:
            logger.warning(f"Serial Port for Triggerduino is None, will not send analog signals!")

    def sendSignal(self, channel, value, duration, lsl_message=None):
        trigger = TriggerStruct(channel=channel, value=value, duration=duration)
        if value not in range(0, 4096): logger.warning("Value should be between 0 and 4095")
        self.sendTrigger(trigger)

        if self.lsl_outlet:
            x = [str(channel), str(value), str(duration), lsl_message if lsl_message else str(value)]
            self.lsl_outlet.push_sample(x=x)
            logger.info(f"Pushed sample via lsl {x}")

    def sendTrigger(self, trigger):
        self.sendTriggers([trigger])

    def sendTriggers(self, triggers):
        triggers_b = bytearray()
        for trigger in triggers:
            triggers_b.extend(bytearray(trigger))

        if self.serial_port:
            self.serial_port.write(triggers_b)
            self.serial_port.flush()
            logger.debug(f"Serial data: {triggers_b}")
        else:
            logger.warning(f"No serial port registered, not sending analog triggers")

        for trigger in triggers:
            logger.info(
                f"Trigger sent: Channel {trigger.channel}, value: {trigger.value}, duration: {trigger.duration}ms");


def monitor_serial(stop, ser):
    while not stop():
        line = ser.readline()
        if line:
            print(line)
