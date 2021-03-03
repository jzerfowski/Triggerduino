#include "DAC.h"

DAC::DAC(uint8_t deviceAddress)
{
    // Constructor requires only the device address for a corresponding MCP4725
    this->mcp4725 = new MCP4725(deviceAddress);
    this->deviceAddress = deviceAddress;
}

void DAC::startTrigger(int value, int duration_ms)
{
    Serial.print(mcp4725->setValue(value));

    until = millis() + duration_ms;
    active = true;
}

void DAC::update()
{
    unsigned long now = millis();
    // Check if DAC is on but should be turned off because time limit is reached
    if (active && now >= until)
    {
        stopTrigger();
    }
}

void DAC::stopTrigger()
{
    mcp4725->setValue(0);
    active = false;
}