# Triggerduino
To synchronize neural data streams from multiple devices, one needs a way to know the temporal shift between them. This is the repository for a handy tool that can generates spikes on an analog channel (0-5V range in 4096 steps). These can also be used as condition markers (e.g., in [mne](https://mne.tools/stable/index.html)). It is plugged in via USB and there is a simple python interface to spike synchronization triggers or experiment markers.

## Hardware
We used an [Arduino Nano](https://www.arduino.cc/en/pmwiki.php?n=Main/ArduinoBoardNano) and 2 [MCP4725](https://www.sparkfun.com/products/12918) 12-bit DACs

## Software
Sources can be found in the corresponding folders. The Arduino C++-Code requires the library [MCP4725](https://github.com/RobTillaart/MCP4725).

The interface to use triggers is in python and needs only [pyserial](https://github.com/pyserial/pyserial)
