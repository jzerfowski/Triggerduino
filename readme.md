# Triggerduino
To synchronize data streams from multiple devices (in my case MEG, EMG and trigger/marker signals), one needs a way to know the temporal shift between them. This is the repository for a handy tool that can generates spikes on an analog channel (0-5V range in steps from 0-4095). These can also be used as condition markers (e.g., in [mne](https://mne.tools/stable/index.html)). It is plugged in via USB and there is a simple python interface to spike synchronization triggers or experiment markers.

## Hardware
We used an [Arduino Nano](https://www.arduino.cc/en/pmwiki.php?n=Main/ArduinoBoardNano) and 2 [MCP4725](https://www.sparkfun.com/products/12918) 12-bit DACs

## Software
Sources can be found in the corresponding folders. The Arduino C++-Code requires the library [MCP4725](https://github.com/RobTillaart/MCP4725).

The interface to use triggers is in python and needs only [pyserial](https://github.com/pyserial/pyserial)

## How it works
To send the information in the most efficient way possible, we only send necessary information to the Arduino. Therefore, we reconstruct the `struct Trigger` in `DAC.h` exactly with our `TriggerStruct` in `triggerduino.py`, which inherits from `ctypes.Structure`. We send this as a bytestream on the serial port which the Arduino interprets as a triggers. Potentially, more information can be sent to the Arduino, but then it is important to keep the order and type of values consistent between python and C.
