/*
 * ChronoA.h
 *
 *  Created on: 15 abr. 2020
 *      Author: killan
 */

#ifndef CHRONOA_H_
#define CHRONOA_H_

#include <msp430.h>
#include <boardMSP.h>
#include <Technique.h>
#include <DACR2R.h>

class ChronoA: public Technique
{
public:
    ChronoA();
    uint16_t NextValue();
    uint16_t getCurrentValue();
    void processData(char *data, int len);
    uint8_t StopCondition();
private:
    /* Variables */
    uint16_t StartValue;
    uint16_t TimeHold;
    uint16_t FinalValue;
    uint16_t CurrentValue;
    uint8_t ScanRate;
    bool Direction = false;
};

#endif /* CHRONOA_H_ */
