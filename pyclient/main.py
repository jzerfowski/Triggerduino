import serial
import time
import logging
from threading import Thread

from triggerduino import Triggerduino, monitor_serial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

num_channels = 2

channels = [0, 1]
period = 0.5  # in s
trigger_duration = 30  # in ms
trigger_value = 4000

stop_thread = False

if __name__ == '__main__':
    running = True

    with serial.Serial('COM6', timeout=0.01, baudrate=115200, write_timeout=0.5) as ser:
        serialMonitor = Thread(target=lambda stop_flag: monitor_serial(stop_flag, ser), args=(lambda: stop_thread,))
        serialMonitor.start()

        trigger = Triggerduino(ser)

        logger.info("Wait 2 seconds for serial port")
        time.sleep(2)

        channels = [0]
        while running:
            for channel in channels:
                trigger.sendSignal(channel, trigger_value, trigger_duration)
            time.sleep(period)
            pass

        stop_thread = False
        serialMonitor.join()
    logger.info("Triggerduino interface shut down")
