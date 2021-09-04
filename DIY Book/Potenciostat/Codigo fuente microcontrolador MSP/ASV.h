/*
 * ASV.h
 *
 *  Created on: Mar 11, 2020
 *      Author: killan
 */

#ifndef ASV_H_
#define ASV_H_

#include <msp430.h>
#include <boardMSP.h>
#include <Technique.h>
#include <DACR2R.h>

class ASV: public Technique
{
public:
    ASV();
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

#endif /* ASV_H_ */
