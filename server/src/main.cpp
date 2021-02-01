#include <Wire.h>
#include <Arduino.h>

#include "MCP4725.h"
#include "DAC.h"


#define NUM_DACS 2  // Number of plugged in DACs

DAC *dac_ch0 = new DAC(0x60);  // Define DAC instances with their respective I2C addresses. We expect MCP4725 here
DAC *dac_ch1 = new DAC(0x61);

DAC *dacs[NUM_DACS] = {dac_ch0, dac_ch1};  // Enumerated access of all DACs

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(2);  // Set a short timeout (in ms) for reading from the Serial port
  // We shouldn't run in the above timeout anyways because we do a check for available bytes, but better safe than sorry!
  
  Serial.print("Triggerduino waking up, welcome!\nI have ");
  Serial.print(NUM_DACS);
  Serial.println(" DAC channels.");

  for (int i = 0; i < NUM_DACS; i++) {
    (dacs[i]->mcp4725)->begin();
    if (!(dacs[i]->mcp4725)->isConnected()) {
      Serial.println("Connection Error");
    }

    dacs[i]->startTrigger(4095, 10000);
  }

};

void loop() {
  Trigger trigger;

  // If there are bytes available, read them and write the result into trigger
  while ((unsigned) Serial.available() >= sizeof(Trigger)) {
    if (Serial.readBytes((char*)&trigger, sizeof(Trigger)) == sizeof(Trigger)) {
      dacs[trigger.channel]->startTrigger(trigger.value, trigger.duration);
      Serial.print(millis());
      Serial.print(" ms: Channel ");
      Serial.print(trigger.channel);
      Serial.print(" trigger with value ");
      Serial.print(trigger.value);
      Serial.print(" and duration ");
      Serial.print(trigger.duration);
      Serial.println(" ms");
    } else {
      Serial.println("Error while receiving trigger");
    }
  }

  // Update all DACs (checks if the "until" value is reached to reset to 0)
  for (int i = 0; i < NUM_DACS; i++) {
    dacs[i]->update();
  }
};