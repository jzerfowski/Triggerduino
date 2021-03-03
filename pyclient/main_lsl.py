import serial
import time
import logging
import random
from pylsl import StreamInfo, StreamOutlet

from triggerduino import Triggerduino, monitor_serial
from threading import Thread

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

num_channels = 2

channels = [0, 1]
period = 0.2  # in s
trigger_duration = 20  # in ms
# trigger_value = 4095

stop_thread = False
trigger_values = list(range(0, 4096, 64))

if __name__ == '__main__':
    with serial.Serial('COM6', timeout=0.01, baudrate=115200, write_timeout=0.5) as ser:
        serialMonitor = Thread(target=lambda stop_flag: monitor_serial(stop_flag, ser), args=(lambda : stop_thread,))
        serialMonitor.start()

        logger.info("Wait 2 seconds for serial port")
        time.sleep(2)
        info = StreamInfo('MyMarkerStream', 'Markers', channel_count=4, nominal_srate=0, channel_format='string', source_id='myuidw43536')

        # next make an outlet
        outlet = StreamOutlet(info)

        trigger = Triggerduino(ser, lsl_outlet=outlet)
        logger.info("Wait 2 seconds for Triggerduino")
        time.sleep(2)

        channels = [1]

        running = True
        while running:
            trigger_value = random.choice(trigger_values)
            for channel in channels:
                trigger.sendSignal(channel, trigger_value, trigger_duration)
            time.sleep(period)
            pass

        stop_thread = False
        serialMonitor.join()
    logger.info("Triggerduino interface shut down")
