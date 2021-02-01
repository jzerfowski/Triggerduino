#ifndef DAC_h
#define DAC_h

#include "Wire.h"
#include "MCP4725.h"

// A pulse is defined by its DAC channel, a value [0-4095] and a duration in ms
struct Trigger {
  int16_t channel;
  int16_t value;
  int16_t duration;
};


class DAC {
    bool active;
    int value;
    unsigned long until;

    public:
        MCP4725 *mcp4725;

        DAC(uint8_t deviceAddress);
        void startTrigger(int value, int duration_ms);
        void update();
        void stopTrigger();
};

#endif