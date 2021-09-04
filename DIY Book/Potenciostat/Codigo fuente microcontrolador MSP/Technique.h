/*
 * Technique.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef TECHNIQUE_H_
#define TECHNIQUE_H_

#include <msp430.h>
#include <DACgenerator.h>
#include <stdint.h>

class Technique
{
public:
    bool isRunning();

    DAC_generator *dac;
    virtual uint16_t getCurrentValue()=0;
    virtual uint16_t NextValue()=0;
    virtual uint8_t StopCondition()=0;
    virtual void processData(char *data, int len)=0;

    bool active = false;
};

#endif /* TECHNIQUE_H_ */
