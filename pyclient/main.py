import serial
import time

from Triggerduino import Triggerduino, monitor_serial
from threading import Thread

import logging
logging.basicConfig(level=logging.INFO)

num_channels = 2

channels = [0, 1]
period = 3  # in s
trigger_duration = 1000  # in ms
trigger_value = 4000

stop_thread = False


if __name__ == '__main__':
    running = True

    with serial.Serial('COM4', timeout=0.01, baudrate=115200, write_timeout=0.5) as ser:
        serialMonitor = Thread(target=lambda stop_flag: monitor_serial(stop_flag, ser), args=(lambda : stop_thread,))
        serialMonitor.start()

        trigger = Triggerduino(ser, 2)

        logging.info("Wait 2 seconds for serial port")
        time.sleep(2)

        while running:
            for channel in channels:
                trigger.sendSignal(channel, trigger_value, trigger_duration)
            time.sleep(period)
            pass

        stop_thread = False
        serialMonitor.join()
    print("Triggerduino interface shut down")